function markUndone(task_id) {
    const task = document.getElementById(`task-${task_id}`);
    
    fetch(`/mark_undone_ajax/${task_id}`, {
        method: "POST"
    })
    .then(response => {
        if(response.ok) {
            task.classList.add("d-none");
        } else {
            alert("Failed to mark task as undone.");
        }
    })
    .catch(e => {
        console.log("Error: ", e)
        alert("Request failed.")
    })
}