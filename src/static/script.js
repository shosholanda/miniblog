function like(id_post){
    // Need to verify 1 like per account
    json = {'id': id_post}

    fetch('like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json) //fuck you
    })
    .then(response => {
        return response.text().then(text => {
            // return JSON.parse(text); // Todos coludos o todos rabones
	    // console.log(text);

	    //ODIO LAS PROMESAS, ME RECUERDAN A MI EX
	    let likes = fetch('get-likes/' + id_post).then(response => {
		return response.json().then( data => {
		    let span = document.getElementById('likes' + id_post);
		    console.log(data['likes']);
		    span.textContent = data['likes'];
		});
	    });
            return text;
        });
    })
    .catch((error) => {
        console.log('Error:', error);
    });
}

window.onload = function() {
    let l = document.getElementsByTagName("span");

    for (let elem of l){
	let id = elem.id.substring(5);
	let e = elem.parentNode;
	e.addEventListener('click', function() {
	    like(id)
	});
    }
}
