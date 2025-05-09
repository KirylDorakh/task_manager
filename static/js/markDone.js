function markDone(task_id) {
    const task = document.getElementById(`task-${task_id}`);
    
    fetch(`/mark_done_ajax/${task_id}`, {
        method: "POST"
    })
    .then(response => {
        if(response.ok) {
            task.classList.add("d-none");
        } else {
            alert("Failed to mark task as done.");
        }
    })
    .catch(e => {
        console.log("Error: ", e)
        alert("Request failed.")
    })
}