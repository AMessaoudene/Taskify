document.addEventListener("DOMContentLoaded", function () {
    const taskForm = document.getElementById("taskForm");
    const taskNameInput = document.getElementById("taskName");
    const taskCategorySelect = document.getElementById("taskCategory");
    const taskDateTimeInput = document.getElementById("taskDateTime");
    const taskList = document.getElementById("taskList");

    // Set the taskDateTimeInput to the current date and time when the page loads
    const currentDateTime = new Date();
    const currentYear = currentDateTime.getFullYear();
    const currentMonth = String(currentDateTime.getMonth() + 1).padStart(2, '0');
    const currentDay = String(currentDateTime.getDate()).padStart(2, '0');
    const currentHour = String(currentDateTime.getHours()).padStart(2, '0');
    const currentMinute = String(currentDateTime.getMinutes()).padStart(2, '0');
    const currentDateTimeString = `${currentYear}-${currentMonth}-${currentDay}T${currentHour}:${currentMinute}`;
    taskDateTimeInput.value = currentDateTimeString;
    taskDateTimeInput.min = currentDateTimeString;

    taskForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const taskName = taskNameInput.value.trim();
        const taskCategory = taskCategorySelect.value;
        const taskDateTime = taskDateTimeInput.value;
        if (taskName !== "") {
            addTask(taskName, taskCategory, taskDateTime);
            taskNameInput.value = "";
            taskDateTimeInput.value = currentDateTimeString; // Reset to current date and time
        }
    });
});
    function addTask(taskName, taskCategory, taskDateTime) {
    const listItem = document.createElement("li");
    listItem.classList.add("list-group-item", `list-group-item-${taskCategory}`);

    const row1 = document.createElement("div");
    row1.classList.add("d-flex", "flex-row", "mb-3");

    const row2 = document.createElement("div");
    row2.classList.add("d-flex", "flex-row");

    // Create columns for the first row
    const nameColumn = document.createElement("div");
    nameColumn.classList.add("col-3", "task-name");
    nameColumn.textContent = taskName;

    const typeColumn = document.createElement("div");
    typeColumn.classList.add("col-3", "task-category");
    typeColumn.textContent = taskCategory;

    const dateHourColumn = document.createElement("div");
    dateHourColumn.classList.add("col-3", "task-date-time");
    dateHourColumn.textContent = new Date(taskDateTime).toLocaleString();

    const statusColumn = document.createElement("div");
    statusColumn.classList.add("col-3", "task-status");

    const taskStatusSelect = document.createElement("select");
    taskStatusSelect.classList.add("form-select");
    taskStatusSelect.innerHTML = `
        <option value="done" style="color: green;background-color:#7FFF89">Done</option>
        <option value="in-progress" style="color: yellow;background-color:#95A100">In Progress</option>
        <option value="not-yet" style="color: red;background-color:#810202">Not Yet</option>
    `;

    statusColumn.appendChild(taskStatusSelect);

    // Create columns for the second row (Edit and Delete buttons)
    const editButtonColumn = document.createElement("div");
    editButtonColumn.classList.add("col-6");

    const editButton = document.createElement("button");
    editButton.classList.add("btn", "btn-light", "btn-sm", "edit-button");
    editButton.innerText = "Edit";
    editButton.addEventListener("click", function () {
        editTask(listItem);
    });

    editButtonColumn.appendChild(editButton);

    const deleteButtonColumn = document.createElement("div");
    deleteButtonColumn.classList.add("col-6");

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("btn", "btn-danger", "btn-sm");
    deleteButton.innerText = "Delete";
    deleteButton.addEventListener("click", function () {
        deleteTask(listItem);
    });

    deleteButtonColumn.appendChild(deleteButton);

    // Append columns to the rows
    row1.appendChild(nameColumn);
    row1.appendChild(typeColumn);
    row1.appendChild(dateHourColumn);
    row1.appendChild(statusColumn);

    row2.appendChild(editButtonColumn);
    row2.appendChild(deleteButtonColumn);

    listItem.appendChild(row1);
    listItem.appendChild(row2);

    // Set the initial status to "Not Yet"
    taskStatusSelect.value = "not-yet";

    taskList.appendChild(listItem);
}


    function editTask(listItem) {
    const nameElement = listItem.querySelector(".task-name");
    const editButton = listItem.querySelector(".edit-button");

    if (editButton.innerText === "Edit") {
        const inputElement = document.createElement("input");
        inputElement.classList.add("form-control", "task-name-input");
        inputElement.value = nameElement.textContent.trim();
        nameElement.style.display = "none";
        listItem.insertBefore(inputElement, listItem.firstChild);
        editButton.innerText = "OK";

        // Change button classes to make it green
        editButton.classList.remove("btn-light");
        editButton.classList.add("btn-success");
        inputElement.focus();
    } else if (editButton.innerText === "OK") {
        const inputElement = listItem.querySelector(".task-name-input");
        nameElement.textContent = inputElement.value.trim();
        nameElement.style.display = "block"; // Adjust this line based on your CSS
        inputElement.remove();
        editButton.innerText = "Edit";

        // Change button classes to make it light
        editButton.classList.remove("btn-success");
        editButton.classList.add("btn-light");
    }
}

    function deleteTask(listItem) {
        if (confirm("Are you sure you want to delete this task?")) {
            listItem.remove();
        }
    };