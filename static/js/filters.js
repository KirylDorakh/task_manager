function filterTask(type) {
    const today = new Date().toISOString().split('T')[0];
    const taskItems = document.querySelectorAll('.task');

    taskItems.forEach(task => {
        const dueDate = task.getAttribute('data-due');
        let shouldShow = false;

        if (type === 'today') {
        shouldShow = dueDate === today;
        } else if (type === 'upcoming') {
        shouldShow = dueDate > today;
        } else if (type === 'overdue') {
        shouldShow = dueDate < today;
        } else if (type === 'all') {
        shouldShow = true;
        }

        if (shouldShow) {
        task.classList.remove('d-none');
        } else {
        task.classList.add('d-none');
        }
    });

    document.querySelectorAll('.nav-link').forEach(btn => btn.classList.remove('fw-bold', 'text-primary'));
    const currentBtn = document.getElementById(`filter-${type}`);
    if (currentBtn) {
        currentBtn.classList.add('fw-bold', 'text-primary');
    }
}