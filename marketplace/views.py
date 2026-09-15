import secrets
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import ChatMessage, ListingReport, MarketplaceProfile, PendingRegistration, Product

User = get_user_model()
MMU_EMAIL_DOMAIN = "@student.mmu.edu.my"
OTP_EXPIRY_MINUTES = 10
RESEND_COOLDOWN_SECONDS = 60
CATEGORY_GROUPS = {
    "📱 Electronics": ["📱 Phones", "💻 Laptops", "📲 Tablets", "🎧 Audio", "⌨️ Computer Accessories", "🔌 Other Electronics"],
    "👕 Fashion & Clothing": ["👔 Men’s Clothing", "👗 Women’s Clothing", "👟 Shoes", "👜 Bags", "⌚ Watches & Accessories", "🧢 Other Fashion"],
    "📚 Books & Education": ["📖 Textbooks", "📕 Reference Books", "🧮 Calculators", "✏️ Stationery", "📝 Study Materials", "🎓 Other Education"],
    "🏠 Furniture & Home": ["🪑 Desks", "💺 Chairs", "🗄️ Storage", "💡 Lighting", "🍳 Kitchen", "🏠 Other Home"],
    "🎮 Gaming": ["🎮 Consoles", "💿 Games", "🕹️ Controllers", "🎧 Gaming Accessories", "🖥️ PC Gaming", "🎮 Other Gaming"],
    "⚽ Sports & Hobbies": ["⚽ Sports Equipment", "🏋️ Fitness Equipment", "🚲 Bicycles", "🎸 Musical Instruments", "🃏 Collectibles", "🎨 Other Hobbies"],
    "💄 Beauty & Personal Care": ["🧴 Skincare", "💇 Haircare", "💄 Makeup", "🌸 Fragrances", "🧼 Personal Care", "💅 Other Beauty"],
    "📦 Others": ["🚗 Vehicles", "🛠️ Services", "🎒 Accessories", "📦 Miscellaneous"],
}


def _products():
    """Use the database while keeping the original template context name."""
    return Product.objects.all().order_by("id")


# =========================
# CLIENT ROUTES
# =========================

def home(request):
    products = _products()

    return render(
        request,
        "client/home.html",
        {
            "products": products,
            "featured_products": products[:4],
        },
    )


def product_list(request):
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "best").strip()
    condition = request.GET.get("condition", "").strip()
    search = request.GET.get("q", "").strip()
    products = _products()
    if category:
        products = products.filter(category=category)
    if condition:
        products = products.filter(condition=condition)
    if search:
        search_terms = search.split()
        for term in search_terms:
            products = products.filter(
                Q(name__icontains=term)
                | Q(category__icontains=term)
                | Q(description__icontains=term)
            )
        products = products.annotate(
            title_relevance=Case(
                When(name__iexact=search, then=Value(0)),
                When(name__istartswith=search, then=Value(1)),
                When(name__icontains=search, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        )

    if sort == "recent":
        products = products.order_by("-created_at")
    elif sort == "price_high":
        products = products.order_by("-price", "id")
    elif sort == "price_low":
        products = products.order_by("price", "id")
    elif search:
        products = products.order_by("title_relevance", "-created_at", "name", "id")
    else:
        products = products.order_by("-created_at", "id")
    return render(
        request,
        "client/products.html",
        {
            "products": products,
            "selected_category": category,
            "selected_sort": sort,
            "selected_condition": condition,
            "search_query": search,
            "condition_choices": Product.CONDITION_CHOICES,
        },
    )


def categories(request):
    return render(request, "client/categories.html", {"category_groups": CATEGORY_GROUPS.items()})


@login_required(login_url="login")
def sell(request):
    subcategories = [subcategory for group in CATEGORY_GROUPS.values() for subcategory in group]
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        category = request.POST.get("category", "").strip()
        price_text = request.POST.get("price", "").strip()
        condition = request.POST.get("condition", "").strip()
        description = request.POST.get("description", "").strip()
        image = request.FILES.get("image")

        try:
            price = Decimal(price_text)
        except (InvalidOperation, TypeError):
            price = Decimal("-1")

        if not name or category not in subcategories:
            messages.error(request, "Enter a product name and choose a valid category.")
        elif price < 0:
            messages.error(request, "Enter a valid non-negative price.")
        elif condition not in dict(Product.CONDITION_CHOICES):
            messages.error(request, "Choose a valid item condition.")
        else:
            Product.objects.create(
                name=name,
                category=category,
                price=price,
                stock=1,
                image=image,
                description=description,
                condition=condition,
                seller=request.user,
            )
            messages.success(request, "Your listing was published successfully.")
            return redirect("product_list")

    return render(
        request,
        "client/sell.html",
        {
            "category_groups": CATEGORY_GROUPS.items(),
            "condition_choices": Product.CONDITION_CHOICES,
        },
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "client/product_detail.html", {"product": product})


@login_required(login_url="login")
def edit_listing(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user != product.seller:
        messages.error(request, "You can only edit your own listings.")
        return redirect("product_detail", product_id=product.id)

    subcategories = [subcategory for group in CATEGORY_GROUPS.values() for subcategory in group]

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        category = request.POST.get("category", "").strip()
        price_text = request.POST.get("price", "").strip()
        condition = request.POST.get("condition", "").strip()
        description = request.POST.get("description", "").strip()
        new_image = request.FILES.get("image")

        try:
            price = Decimal(price_text)
        except (InvalidOperation, TypeError):
            price = Decimal("-1")

        if not name or category not in subcategories:
            messages.error(request, "Enter a product name and choose a valid category.")
        elif price < 0:
            messages.error(request, "Enter a valid non-negative price.")
        elif condition not in dict(Product.CONDITION_CHOICES):
            messages.error(request, "Choose a valid item condition.")
        else:
            product.name = name
            product.category = category
            product.price = price
            product.condition = condition
            product.description = description
            if new_image:
                product.image = new_image
            product.save()
            messages.success(request, "Your listing was updated successfully.")
            return redirect("product_detail", product_id=product.id)

    return render(
        request,
        "client/edit_listing.html",
        {
            "product": product,
            "category_groups": CATEGORY_GROUPS.items(),
            "condition_choices": Product.CONDITION_CHOICES,
        },
    )


@login_required(login_url="login")
@require_POST
def delete_listing(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user != product.seller:
        messages.error(request, "You can only delete your own listings.")
        return redirect("product_detail", product_id=product.id)

    product.delete()
    messages.success(request, "Your listing was deleted successfully.")
    return redirect("product_list")


@require_POST
def report_listing(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reason = request.POST.get("reason", "").strip()
    details = request.POST.get("details", "").strip()
    valid_reasons = dict(ListingReport.REASON_CHOICES)

    if reason not in valid_reasons:
        messages.error(request, "Choose a reason before submitting your report.")
    elif reason == "other" and not details:
        messages.error(request, "Please describe the issue when choosing Other.")
    else:
        ListingReport.objects.create(
            product=product,
            reporter=request.user if request.user.is_authenticated else None,
            reason=reason,
            details=details,
        )
        messages.success(request, "Thanks. Your report has been sent to the marketplace team.")

    return redirect("product_detail", product_id=product.id)


def cart(request):
    cart_items = _cart_items(request)
    total = sum(item["subtotal"] for item in cart_items)
    return render(request, "client/cart.html", {"cart_items": cart_items, "total": total})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock < 1:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect("product_detail", product_id=product.id)

    cart_data = request.session.get("cart", {})
    product_key = str(product.id)
    cart_data[product_key] = 1
    request.session["cart"] = cart_data
    request.session.modified = True
    messages.success(request, f"{product.name} was added to your cart.")
    return redirect(request.POST.get("next") or "cart")


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    cart_data = request.session.get("cart", {})
    product_key = str(product.id)
    if quantity > 0 and product.stock > 0:
        cart_data[product_key] = min(quantity, product.stock)
    else:
        cart_data.pop(product_key, None)
    request.session["cart"] = cart_data
    request.session.modified = True
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    cart_data.pop(str(product_id), None)
    request.session["cart"] = cart_data
    request.session.modified = True
    return redirect("cart")


def _cart_items(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart_data.keys())
    items = []
    cleaned_cart = {}
    for product in products:
        quantity = 1 if product.stock > 0 else 0
        if quantity:
            cleaned_cart[str(product.id)] = 1
            items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "subtotal": product.price,
                }
            )
    if cleaned_cart != cart_data:
        request.session["cart"] = cleaned_cart
        request.session.modified = True
    return items


@login_required(login_url="login")
def product_chat(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            ChatMessage.objects.create(
                product=product,
                buyer=request.user,
                seller=product.seller,
                message=message,
            )
            messages.success(request, "Your message was sent to the seller.")
            return redirect("product_chat", product_id=product.id)
        messages.error(request, "Write a message before sending.")

    chat_messages = ChatMessage.objects.filter(product=product, buyer=request.user)
    seller_name = product.seller.get_full_name() or product.seller.email if product.seller else "Marketplace seller"
    return render(
        request,
        "client/chat.html",
        {"product": product, "chat_messages": chat_messages, "seller_name": seller_name},
    )


def checkout(request):
    return render(request, "client/checkout.html")


def order_confirmation(request):
    return render(request, "client/order_confirmation.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not subject or not message:
            messages.error(request, "Please complete all fields before sending your message.")
        else:
            send_mail(
                subject=f"MMU Marketplace: {subject}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=None,
                recipient_list=["support@mmu-marketplace.local"],
                fail_silently=True,
            )
            messages.success(request, "Thanks. Your message has been sent to the marketplace support team.")
            return redirect("contact")

    return render(request, "client/contact.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
        else:
            auth_login(request, user)
            return redirect("profile")

    return render(request, "client/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not email.endswith(MMU_EMAIL_DOMAIN):
            messages.error(request, "Registration is limited to MMU student email accounts.")
        elif password != confirm_password:
            messages.error(request, "Password and confirm password must match.")
        elif not name or len(password) < 8:
            messages.error(request, "Enter your name and a password of at least 8 characters.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            pending = PendingRegistration.objects.filter(email=email).first()
            if pending and timezone.now() - pending.otp_created_at < timedelta(seconds=RESEND_COOLDOWN_SECONDS):
                messages.error(request, "An OTP was just sent. Please wait before requesting another one.")
            else:
                otp = _new_otp()
                now = timezone.now()
                if pending is None:
                    pending = PendingRegistration(email=email, name=name)
                pending.name = name
                pending.password = make_password(password)
                pending.otp_hash = make_password(otp)
                pending.otp_created_at = now
                pending.expires_at = now + timedelta(minutes=OTP_EXPIRY_MINUTES)
                pending.save()
                _send_otp(email, otp)
                request.session["pending_registration_id"] = pending.id
                messages.success(request, f"An OTP was sent to {email}.")
                return redirect("verify_registration")

    return render(request, "client/register.html")


def verify_registration(request):
    pending = _pending_from_session(request)
    if pending is None:
        messages.error(request, "Start registration again to request an OTP.")
        return redirect("register")

    if request.method == "POST":
        otp = request.POST.get("otp", "").strip()
        if timezone.now() > pending.expires_at:
            messages.error(request, "This OTP has expired. Request a new one.")
        elif not check_password(otp, pending.otp_hash):
            messages.error(request, "The OTP is incorrect.")
        else:
            user = User(
                username=pending.email,
                email=pending.email,
                password=pending.password,
                first_name=pending.name,
            )
            user.save()
            MarketplaceProfile.objects.create(user=user)
            pending.delete()
            request.session.pop("pending_registration_id", None)
            auth_login(request, user)
            messages.success(request, "Your account is verified. You can now buy and sell on MMU Marketplace.")
            return redirect("profile")

    return render(request, "client/verify_registration.html", {"email": pending.email})


@require_POST
def resend_registration_otp(request):
    pending = _pending_from_session(request)
    if pending is None:
        messages.error(request, "Start registration again to request an OTP.")
        return redirect("register")

    elapsed = timezone.now() - pending.otp_created_at
    if elapsed < timedelta(seconds=RESEND_COOLDOWN_SECONDS):
        remaining = RESEND_COOLDOWN_SECONDS - int(elapsed.total_seconds())
        messages.error(request, f"Please wait {remaining} seconds before requesting another OTP.")
        return redirect("verify_registration")

    otp = _new_otp()
    pending.otp_hash = make_password(otp)
    pending.otp_created_at = timezone.now()
    pending.expires_at = pending.otp_created_at + timedelta(minutes=OTP_EXPIRY_MINUTES)
    pending.save(update_fields=["otp_hash", "otp_created_at", "expires_at"])
    _send_otp(pending.email, otp)
    messages.success(request, "A new OTP was sent to your email.")
    return redirect("verify_registration")


def _new_otp():
    return f"{secrets.randbelow(1_000_000):06d}"


def _pending_from_session(request):
    pending_id = request.session.get("pending_registration_id")
    if not pending_id:
        return None
    return PendingRegistration.objects.filter(id=pending_id).first()


def _send_otp(email, otp):
    send_mail(
        "MMU Marketplace registration OTP",
        f"Your MMU Marketplace verification code is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes.",
        None,
        [email],
    )


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required(login_url="login")
def account_settings(request):
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "email":
            new_email = request.POST.get("new_email", "").strip().lower()
            confirm_email = request.POST.get("confirm_email", "").strip().lower()
            if not new_email or not confirm_email:
                messages.error(request, "Please enter both email fields.")
            elif new_email != confirm_email:
                messages.error(request, "The new email addresses do not match.")
            elif new_email == request.user.email.lower():
                messages.error(request, "This is already your current email address.")
            elif not new_email.endswith(MMU_EMAIL_DOMAIN):
                messages.error(request, "Only MMU student emails can be used.")
            elif User.objects.filter(email__iexact=new_email).exclude(pk=request.user.pk).exists():
                messages.error(request, "This email is already in use.")
            else:
                otp = _new_otp()
                request.session["pending_account_change"] = {
                    "type": "email",
                    "new_email": new_email,
                    "otp_hash": make_password(otp),
                    "expires_at": (timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)).isoformat(),
                    "sent_to": new_email,
                }
                send_mail(
                    "MMU Marketplace account email change OTP",
                    f"Your verification code is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes.",
                    None,
                    [new_email],
                )
                messages.success(request, f"A verification code was sent to {new_email}.")
                return redirect("verify_account_change")

        elif action == "password":
            current_password = request.POST.get("current_password", "")
            new_password = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")
            if not request.user.check_password(current_password):
                messages.error(request, "Your current password is incorrect.")
            elif not new_password or len(new_password) < 8:
                messages.error(request, "New password must be at least 8 characters long.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                otp = _new_otp()
                request.session["pending_account_change"] = {
                    "type": "password",
                    "new_password": make_password(new_password),
                    "otp_hash": make_password(otp),
                    "expires_at": (timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)).isoformat(),
                    "sent_to": request.user.email,
                }
                send_mail(
                    "MMU Marketplace account password change OTP",
                    f"Your verification code is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes.",
                    None,
                    [request.user.email],
                )
                messages.success(request, f"A verification code was sent to {request.user.email}.")
                return redirect("verify_account_change")

    return render(request, "client/account_settings.html")


@login_required(login_url="login")
def verify_account_change(request):
    pending = request.session.get("pending_account_change")
    if not pending:
        messages.error(request, "No account change is pending.")
        return redirect("account_settings")

    if request.method == "POST":
        otp = request.POST.get("otp", "").strip()
        expires_at = timezone.datetime.fromisoformat(pending["expires_at"]) if isinstance(pending.get("expires_at"), str) else pending.get("expires_at")
        if timezone.now() > expires_at:
            messages.error(request, "This verification code has expired. Please request a new one.")
            request.session.pop("pending_account_change", None)
            return redirect("account_settings")
        if not check_password(otp, pending["otp_hash"]):
            messages.error(request, "The verification code is incorrect.")
            return redirect("verify_account_change")

        user = request.user
        if pending["type"] == "email":
            user.email = pending["new_email"]
            user.username = pending["new_email"]
            user.save(update_fields=["email", "username"])
            messages.success(request, "Your email address was updated successfully.")
        elif pending["type"] == "password":
            user.password = pending["new_password"]
            user.save(update_fields=["password"])
            messages.success(request, "Your password was updated successfully.")

        request.session.pop("pending_account_change", None)
        return redirect("profile")

    return render(request, "client/verify_account_change.html", {"email": pending.get("sent_to", request.user.email)})


@login_required(login_url="login")
def profile(request):
    profile_obj, _ = MarketplaceProfile.objects.get_or_create(user=request.user)

    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile_obj.profile_picture = request.FILES["profile_picture"]
        profile_obj.save(update_fields=["profile_picture"])
        messages.success(request, "Your profile picture has been updated.")
        return redirect("profile")

    selling_products = Product.objects.filter(seller=request.user).order_by("-created_at")
    purchased_ids = request.session.get("purchased_products", [])
    buying_products = list(Product.objects.filter(id__in=purchased_ids).order_by("-created_at")) if purchased_ids else []

    initials = "".join(part[0].upper() for part in request.user.get_full_name().split()[:2]) if request.user.get_full_name() else request.user.email[0].upper()

    return render(
        request,
        "client/profile.html",
        {
            "profile_obj": profile_obj,
            "selling_products": selling_products,
            "buying_products": buying_products,
            "profile_initials": initials,
        },
    )


# =========================
# ADMIN ROUTES
# =========================

def admin_login(request):
    return render(request, "admin/login.html")


def admin_dashboard(request):
    return render(request, "admin/dashboard.html", {"products": _products()})


def admin_products(request):
    return render(request, "admin/products.html", {"products": _products()})


def add_product(request):
    return render(request, "admin/add_product.html")


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "admin/edit_product.html", {"product": product})


def admin_orders(request):
    return render(request, "admin/orders.html")


def admin_order_detail(request, order_id):
    return render(request, "admin/order_detail.html", {"order_id": order_id})


def admin_users(request):
    return render(request, "admin/users.html")
