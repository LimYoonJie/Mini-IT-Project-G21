const themeToggle = document.querySelector("[data-theme-toggle]");
const documentRoot = document.documentElement;

const setTheme = (theme) => {
	documentRoot.dataset.theme = theme;
	localStorage.setItem("mmuTheme", theme);
};

if (themeToggle) {
	themeToggle.checked = documentRoot.dataset.theme === "dark";
	themeToggle.addEventListener("change", () => {
		setTheme(themeToggle.checked ? "dark" : "light");
	});
}

const accountButton = document.getElementById("account-button");
const accountModal = document.getElementById("account-modal");

if (accountButton && accountModal) {
	const isAccountDropdown = accountButton.getAttribute("aria-haspopup") === "menu";
	const closeAccountModal = () => {
		accountModal.hidden = true;
		accountButton.setAttribute("aria-expanded", "false");
		accountButton.focus();
	};

	accountButton.addEventListener("click", () => {
		const isOpening = accountModal.hidden;
		accountModal.hidden = !isOpening;
		accountButton.setAttribute("aria-expanded", String(isOpening));
		if (isOpening) accountModal.querySelector("a").focus();
	});

	accountModal.querySelectorAll("[data-close-account-modal]").forEach((element) => {
		element.addEventListener("click", closeAccountModal);
	});

	if (isAccountDropdown) {
		document.addEventListener("click", (event) => {
			if (!accountModal.hidden && !accountButton.closest(".account-dropdown").contains(event.target)) {
				closeAccountModal();
			}
		});
	}

	document.addEventListener("keydown", (event) => {
		if (event.key === "Escape" && !accountModal.hidden) {
			closeAccountModal();
		}
	});
}

const faqChat = document.getElementById("faq-chat");
const faqToggle = document.getElementById("faq-chat-toggle");
const faqPanel = document.getElementById("faq-chat-panel");
const faqMinimize = document.getElementById("faq-chat-minimize");
const faqClose = document.getElementById("faq-chat-close");
const faqForm = document.getElementById("faq-chat-form");
const faqInput = document.getElementById("faq-chat-input");
const faqMessages = document.getElementById("faq-chat-messages");

const faqAnswers = [
	{
		keywords: ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
		answer: "Hello! How can I help you with the MMU Marketplace today?",
	},
	{
		keywords: ["register", "sign up", "create account"],
		answer: "Select Account, then Register. Enter your name, MMU student email, and a password, then verify the OTP sent to your email.",
	},
	{
		keywords: ["student email", "mmu email", "email needed", "why email"],
		answer: "Your MMU student email helps us keep the marketplace limited to the MMU community and makes accounts more trustworthy.",
	},
	{
		keywords: ["otp", "verify", "verification code", "one time password"],
		answer: "Enter the OTP from your MMU student email on the verification page before it expires. If it has expired, use the resend option to request a new code.",
	},
	{
		keywords: ["buy", "purchase", "order", "shop"],
		answer: "Browse Products, open an item, and add it to your cart. When you are ready, open Cart and follow the checkout steps.",
	},
	{
		keywords: ["sell", "listing", "list an item", "post item", "create a listing"],
		answer: "Choose Sell in the navigation, sign in with your MMU account, complete the item details, and submit your listing for other students to browse.",
	},
	{
		keywords: ["edit listing", "edit my listing", "change listing", "update listing"],
		answer: "Open your account profile and choose your listing from your products. Select Edit, update the details, and save your changes.",
	},
	{
		keywords: ["delete listing", "delete my listing", "remove listing"],
		answer: "Open your listing from your account profile and choose Delete. Confirm the action only when you are sure, because the listing will no longer be available.",
	},
	{
		keywords: ["payment", "pay", "checkout", "card"],
		answer: "Add an item to your cart, continue to checkout, and review your order before confirming. For payment issues, contact support.",
	},
	{
		keywords: ["delivery", "shipping", "pickup", "collect", "handover"],
		answer: "Arrange the handover details directly with the seller after purchase. You can agree on a suitable MMU pickup point or delivery arrangement.",
	},
	{
		keywords: ["search", "find product", "find item", "look for"],
		answer: "Open Products and use the search field to search by product name, category, or description. You can also filter by category and condition.",
	},
	{
		keywords: ["manage account", "profile", "account", "password", "forgot", "login", "log in"],
		answer: "Use Account to log in or register. From your profile, you can review your details, listings, orders, and account activity.",
	},
	{
		keywords: ["report", "seller", "scam", "fraud", "bad listing", "inappropriate"],
		answer: "Please contact the marketplace team with the seller or listing details and explain the issue so we can investigate it.",
	},
];

const setFaqChatOpen = (isOpen) => {
	if (!faqChat || !faqToggle || !faqPanel) return;
	faqPanel.hidden = !isOpen;
	faqToggle.hidden = isOpen;
	faqToggle.setAttribute("aria-expanded", String(isOpen));
	faqChat.classList.toggle("is-open", isOpen);
	if (isOpen && faqInput) faqInput.focus();
};

const addFaqMessage = (message, isBot = true, showContactLink = false) => {
	if (!faqMessages) return;
	const bubble = document.createElement("div");
	bubble.className = `faq-message ${isBot ? "faq-message-bot" : "faq-message-user"}`;
	bubble.textContent = message;
	faqMessages.appendChild(bubble);

	if (showContactLink) {
		const contactLink = document.createElement("a");
		contactLink.className = "faq-contact-link";
		contactLink.href = "/contact";
		contactLink.textContent = "Contact us";
		faqMessages.appendChild(contactLink);
	}

	faqMessages.scrollTop = faqMessages.scrollHeight;
};

const showFaqTyping = () => {
	if (!faqMessages) return null;
	const typingBubble = document.createElement("div");
	typingBubble.className = "faq-message faq-message-bot faq-message-typing";
	typingBubble.textContent = "...";
	faqMessages.appendChild(typingBubble);
	faqMessages.scrollTop = faqMessages.scrollHeight;
	return typingBubble;
};

const answerFaqQuestion = (question) => {
	const normalizedQuestion = question.toLowerCase();
	const greetingPattern = /\b(hello|hi|hey|good morning|good afternoon|good evening)\b/;
	const matchedFaq = greetingPattern.test(normalizedQuestion)
		? faqAnswers[0]
		: faqAnswers.slice(1).find((faq) => faq.keywords.some((keyword) => normalizedQuestion.includes(keyword)));
	const typingBubble = showFaqTyping();
	window.setTimeout(() => {
		if (typingBubble) typingBubble.remove();
		if (matchedFaq) {
			addFaqMessage(matchedFaq.answer);
			return;
		}
		addFaqMessage("That question needs a little more help from our team. Please contact us and we will get back to you.", true, true);
	}, 1500);
};

if (faqToggle && faqPanel) {
	faqToggle.addEventListener("click", () => setFaqChatOpen(faqPanel.hidden));
	faqMinimize.addEventListener("click", () => setFaqChatOpen(false));
	faqClose.addEventListener("click", () => setFaqChatOpen(false));
	document.querySelectorAll("[data-open-faq-chat]").forEach((link) => {
		link.addEventListener("click", (event) => {
			event.preventDefault();
			setFaqChatOpen(true);
		});
	});

	document.querySelectorAll("[data-faq-question]").forEach((button) => {
		button.addEventListener("click", () => {
			const question = button.dataset.faqQuestion;
			addFaqMessage(question, false);
			answerFaqQuestion(question);
		});
	});

	faqForm.addEventListener("submit", (event) => {
		event.preventDefault();
		const question = faqInput.value.trim();
		if (!question) return;
		addFaqMessage(question, false);
		faqInput.value = "";
		answerFaqQuestion(question);
	});
}

document.querySelectorAll("[data-report-open]").forEach((button) => {
	button.addEventListener("click", () => {
		const reportModal = document.getElementById(button.dataset.reportOpen);
		if (reportModal) reportModal.removeAttribute("hidden");
	});
});

document.querySelectorAll("[data-report-close]").forEach((element) => {
	element.addEventListener("click", () => {
		const reportModal = element.closest(".report-modal");
		if (reportModal) reportModal.setAttribute("hidden", "");
	});
});

document.querySelectorAll("[data-report-reason]").forEach((select) => {
	select.addEventListener("change", () => {
		const reportForm = select.closest(".report-form");
		const details = reportForm.querySelector("[data-report-details]");
		const detailsLabel = reportForm.querySelector("[data-report-details-label]");
		const isOther = select.value === "other";
		details.hidden = !isOther;
		detailsLabel.hidden = !isOther;
		details.required = isOther;
	});
});
