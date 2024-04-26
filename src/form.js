document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var title = document.getElementById('title').value;
    var size = document.getElementById('size').value;
    var type = document.getElementById('type').value;
    var number_bedroom = document.getElementById('number_bedroom').value;
    var location = document.getElementById('location').value;
    var description = document.getElementById('description').value;
    var pictures = document.getElementById('pictures').value;
    var drawing = document.getElementById('drawing').value;
    var price = document.getElementById('price').value;

    var data = {
        title: title,
        size: size,
        type: type,
        number_bedroom: number_bedroom,
        location: location,
        description: description,
        pictures: pictures,
        drawing: drawing,
        price: price
    };

    fetch('/enregistrer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        console.log('Données envoyées avec succès.');
    }).catch(error => {
        console.error('Erreur lors de l\'envoi des données:', error);
    });
});
