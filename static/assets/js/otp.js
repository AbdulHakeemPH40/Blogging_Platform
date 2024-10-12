document.addEventListener("DOMContentLoaded", function() {
    const otpInputs = document.querySelectorAll(".otp-input");

    otpInputs.forEach((input, index) => {
        input.addEventListener("input", function() {
            // Move to the next input if the current one is filled
            if (input.value.length === input.maxLength && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        // Ensure that only numeric input is allowed
        input.addEventListener("keypress", function(event) {
            if (event.which < 48 || event.which > 57) {
                event.preventDefault(); // Prevent non-numeric input
            }
        });

        // Handle backspace to move to the previous input
        input.addEventListener("keydown", function(event) {
            if (event.key === "Backspace" && input.value.length === 0 && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
});
