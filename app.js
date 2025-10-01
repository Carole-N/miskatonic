const form = document.querySelector(`#`);

function handleSubmit(event) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	for (let keyValue of formData.entries()) {
		console.log(keyValue);
	}
}

function toggleInput(field) {
	const select = document.getElementById(field);
	const input = document.getElementById(field + "_input");
	if (select.value === "Autre") {
		input.style.display = "block";
	} else {
		input.style.display = "none";
		input.value = "";
	}
}
