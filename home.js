document.addEventListener("DOMContentLoaded", function () {
    const taskForm = document.getElementById("taskForm");
    const taskNameInput = document.getElementById("taskName");
    const taskCategorySelect = document.getElementById("taskCategory");
    const taskDateTimeInput = document.getElementById("taskDateTime");
    const taskList = document.getElementById("taskList");

    taskForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const taskName = taskNameInput.value.trim();
        const taskCategory = taskCategorySelect.value;
        const taskDateTime = taskDateTimeInput.value;
        if (taskName !== "") {
            addTask(taskName, taskCategory, taskDateTime);
            taskNameInput.value = "";
            taskDateTimeInput.value = "";
        }
    });

    function addTask(taskName, taskCategory, taskDateTime) {
    const listItem = document.createElement("li");
    listItem.classList.add("list-group-item", `list-group-item-${taskCategory}`);

    const nameElement = document.createElement("span");
    nameElement.classList.add("task-name");
    nameElement.textContent = taskName;

    const categoryElement = document.createElement("span");
    categoryElement.classList.add("task-category");
    categoryElement.textContent = taskCategory;

    const dateTimeElement = document.createElement("span");
    dateTimeElement.classList.add("task-date-time");
    dateTimeElement.textContent = new Date(taskDateTime).toLocaleString();

    const taskStatusSelect = document.createElement("select");
    taskStatusSelect.classList.add("form-select", "task-status");
    taskStatusSelect.innerHTML = `
        <option value="done" style="color: green;">Done</option>
        <option value="in-progress" style="color: yellow;">In Progress</option>
        <option value="not-yet" style="color: red;">Not Yet</option>
    `;

    const editButton = document.createElement("button");
    editButton.classList.add("btn", "btn-light", "btn-sm", "mx-2", "edit-button");
    editButton.innerText = "Edit";
    editButton.addEventListener("click", function () {
        editTask(listItem);
    });

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("btn", "btn-danger", "btn-sm");
    deleteButton.innerText = "Delete";
    deleteButton.addEventListener("click", function () {
        deleteTask(listItem);
    });

    listItem.appendChild(nameElement);
    listItem.appendChild(categoryElement);
    listItem.appendChild(dateTimeElement);
    listItem.appendChild(taskStatusSelect);
    listItem.appendChild(editButton);
    listItem.appendChild(deleteButton);

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
        inputElement.value = nameElement.textContent;
        nameElement.style.display = "none";
        listItem.insertBefore(inputElement, nameElement);
        editButton.innerText = "OK";

        // Change button classes to make it green
        editButton.classList.remove("btn-light");
        editButton.classList.add("btn-success");
        inputElement.focus();
    } else if (editButton.innerText === "OK") {
        const inputElement = listItem.querySelector(".task-name-input");
        nameElement.textContent = inputElement.value;
        nameElement.style.display = "inline";
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
    }
});
