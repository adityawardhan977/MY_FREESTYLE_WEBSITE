const taskInput = document.getElementById("taskInput");
const addButton = document.getElementById("addButton");
const taskList = document.getElementById("taskList");
const clearButton = document.getElementById("clearButton");
const taskCount = document.getElementById("taskCount");


addButton.addEventListener("click", addTask);


function addTask() {

    const taskText = taskInput.value.trim();

    if (taskText === "") {
        alert("Please enter a task.");
        return;
    }

    const li = document.createElement("li");

    li.classList.add("task");

    li.innerHTML = `
        <span>${taskText}</span>
        <button class="deleteButton">Delete</button>
    `;

    taskList.appendChild(li);

    taskInput.value = "";

    updateTaskCount();
}


taskList.addEventListener("click", function(event) {

    if (event.target.classList.contains("deleteButton")) {

        event.target.parentElement.remove();

        updateTaskCount();
    }

    else if (event.target.tagName === "SPAN") {

        event.target.parentElement.classList.toggle("completed");
    }

});


clearButton.addEventListener("click", function() {

    taskList.innerHTML = "";

    updateTaskCount();

});


function updateTaskCount() {

    const numberOfTasks = taskList.children.length;

    taskCount.textContent = "Tasks: " + numberOfTasks;
}