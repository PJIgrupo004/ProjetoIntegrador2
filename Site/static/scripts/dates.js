function formatDateToLocalString(date) {
    const offset = -3 * 60; // GMT-3
    const localDate = new Date(date.getTime() + offset * 60 * 1000);
    return localDate.toISOString().slice(0, 16); // YYYY-MM-DDTHH:MM
}

function setMinMaxDate(inputFields) {
    const now = new Date();
    const totalYearsAhead = 1;
    const todayMin = formatDateToLocalString(now);
    const todayMax = formatDateToLocalString(new Date(now.getFullYear() + totalYearsAhead, now.getMonth(), now.getDate()));

    for (const inputField of inputFields) {
        const inputElement = document.getElementById(inputField);
        if (inputElement) {
            inputElement.min = todayMin;
            inputElement.max = todayMax;
            console.log(`Setting min/max for ${inputField}: ${todayMin} - ${todayMax}`); // Debugging
        }
    }
}
