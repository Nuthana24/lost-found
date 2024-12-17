document.addEventListener("DOMContentLoaded", () => {
    const itemsList = document.getElementById('itemsList'); // For index.html (homepage)
    const adminTable = document.getElementById('adminTable') ? document.getElementById('adminTable').getElementsByTagName('tbody')[0] : null; // For admin.html
    const editForm = document.getElementById('editForm');
    const editItemForm = document.getElementById('editItemForm');

    // Only add event listener if reportForm exists (i.e., on report.html)
    const reportForm = document.getElementById('reportForm');
    if (reportForm) {
        reportForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const item = {
                image: document.getElementById('itemImage').value,
                title: document.getElementById('itemTitle').value,
                category: document.getElementById('itemCategory').value,
                description: document.getElementById('itemDescription').value,
                location: document.getElementById('itemLocation').value,
                contactInfo: document.getElementById('contactInfo').value,
                status: document.getElementById('itemStatus').value
            };

            let items = JSON.parse(localStorage.getItem('items')) || [];
            items.push(item); // Add new item to the list
            localStorage.setItem('items', JSON.stringify(items)); // Save to localStorage

            // Optionally clear the form
            reportForm.reset();

            // Reload the items on the homepage
            window.location.href = "index.html"; // Redirect to homepage
        });
    }

    // Load items from localStorage
    function loadItems() {
        let items = JSON.parse(localStorage.getItem('items')) || [];

        // Display items on the homepage (index.html)
        if (itemsList) {
            itemsList.innerHTML = '';
            items.forEach((item) => {
                const itemCard = document.createElement('div');
                itemCard.classList.add('card');
                itemCard.innerHTML = `
                    <img src="${item.image}" alt="${item.title}">
                    <div class="title">${item.title}</div>
                    <div class="category">${item.category}</div>
                    <div class="description">${item.description}</div>
                    <div class="location">${item.location}</div>
                `;
                itemsList.appendChild(itemCard);
            });
        }

        // Display items in the admin panel (admin.html)
        if (adminTable) {
            adminTable.innerHTML = '';
            items.forEach((item, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.status}</td>
                    <td><img src="${item.image}" alt="${item.title}" width="50"></td>
                    <td>${item.title}</td>
                    <td>${item.category}</td>
                    <td>${item.description}</td>
                    <td>${item.location}</td>
                    <td>${item.contactInfo}</td>
                    <td>
                        <button class="edit" onclick="editItem(${index})">Edit</button>
                        <button class="delete" onclick="deleteItem(${index})">Delete</button>
                    </td>
                `;
                adminTable.appendChild(row);
            });
        }
    }

    // Edit item
    window.editItem = (index) => {
        let items = JSON.parse(localStorage.getItem('items')) || [];
        const item = items[index];
        
        // Fill the edit form with the selected item details
        document.getElementById('editItemStatus').value = item.status;
        document.getElementById('editItemImage').value = item.image;
        document.getElementById('editItemTitle').value = item.title;
        document.getElementById('editItemCategory').value = item.category;
        document.getElementById('editItemDescription').value = item.description;
        document.getElementById('editItemLocation').value = item.location;
        document.getElementById('editContactInfo').value = item.contactInfo;

        // Show the edit form
        editForm.style.display = 'block';

        // Save the item after editing
        editItemForm.onsubmit = function(e) {
            e.preventDefault();

            // Update the item with the new values from the form
            item.status = document.getElementById('editItemStatus').value;
            item.image = document.getElementById('editItemImage').value;
            item.title = document.getElementById('editItemTitle').value;
            item.category = document.getElementById('editItemCategory').value;
            item.description = document.getElementById('editItemDescription').value;
            item.location = document.getElementById('editItemLocation').value;
            item.contactInfo = document.getElementById('editContactInfo').value;

            // Save the updated items list back to localStorage
            items[index] = item;
            localStorage.setItem('items', JSON.stringify(items));

            // Hide the edit form and reload the items
            editForm.style.display = 'none';
            loadItems(); // Refresh the item list to reflect changes in both admin and homepage
        };
    };

    // Cancel edit
    window.cancelEdit = () => {
        editForm.style.display = 'none';
    };

    // Delete item
    window.deleteItem = (index) => {
        let items = JSON.parse(localStorage.getItem('items')) || [];
        items.splice(index, 1);
        localStorage.setItem('items', JSON.stringify(items));
        loadItems(); // Reload items after deleting
    };

    loadItems(); // Initial load
});
