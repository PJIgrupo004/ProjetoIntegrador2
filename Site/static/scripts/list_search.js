window.onload = function() {
    const dateInput = document.getElementById('dataInput')
    const today = new Date()
    const year = today.getFullYear()
    const month = String(today.getMonth() + 1).padStart(2, '0')
    const day = String(today.getDate()).padStart(2, '0')

    dateInput.value = `${year}-${month}-${day}`
    filterDateTable(dateInput.value)
};



function filterTable() {
    const input = document.getElementById("filterInput")
    const filter = input.value.toLowerCase()
    const table = document.getElementById("clientsTable")
    const rows = table.getElementsByTagName("tr")
    let visibleRows = []

    for (let i = 1; i < rows.length; i++) { // Ignorar o cabeçalho
        const cells = rows[i].getElementsByTagName("td")
        let rowVisible = false;

        for (let j = 0; j < cells.length; j++) {
            const cellValue = cells[j].textContent.toLowerCase()
            if (cellValue.includes(filter)) {
                rowVisible = true
                break
            }
        }

        rows[i].style.display = rowVisible ? "" : "none"

        if (rowVisible) {
            visibleRows.push(rows[i])
        }
    }

    return visibleRows
}

function filterDateTable() {
    const selectedDate = document.getElementById("dataInput").value
    const visibleRows = filterTable()

    for (let i = 0; i < visibleRows.length; i++) {
        const rowDate = visibleRows[i].getAttribute('data-date')
        const [date, time] = rowDate.split(' ')
        const rowVisible = date === selectedDate;

        visibleRows[i].style.display = rowVisible ? "" : "none"
    }
}

function clearFilter() {
    const filterInput = document.getElementById('filterInput')
    filterInput.value = ''
    filterTable()
}

function deleteOnList(id, url, message) {
    if (confirm(message)) {
        fetch(`/${url}/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                response.json().then(errorData => {
                    console.log(errorData.error);
                });
            }
            window.location.href = `/${url}`;
        })
        .catch(error => {
            console.log(error);
        });
    }
}

function editObj(obj, id_field, url) {
    console.log(obj)
    window.location.href = `/${url}/${obj[id_field]}`;
}
