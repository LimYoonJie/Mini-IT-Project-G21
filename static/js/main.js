const accountButton = document.getElementById("account-button");
const accountModal = document.getElementById("account-modal");

if (accountButton && accountModal) {
	const closeAccountModal = () => {
		accountModal.hidden = true;
		accountButton.focus();
	};

	accountButton.addEventListener("click", () => {
		accountModal.removeAttribute("hidden");
		accountModal.querySelector("a").focus();
	});

	accountModal.querySelectorAll("[data-close-account-modal]").forEach((element) => {
		element.addEventListener("click", closeAccountModal);
	});

	document.addEventListener("keydown", (event) => {
		if (event.key === "Escape" && !accountModal.hidden) {
			closeAccountModal();
		}
	});
}
