// this Js doc is the client-side for the message board/

// this event is triggered when the HTML has been completely loaded, and then connects to the web socket
document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // checking if there is a message input of so, sends text to server then clears message input
    document.getElementById('message-board-form').onsubmit = function(e) {
        e.preventDefault();
        let inputMessage = document.getElementById('message-board-input');
        if (inputMessage.value.length > 0) {
            socket.emit('post_message',{text: inputMessage.value});
            inputMessage.value = '';
        }

    };
    // listener for new message events emitted from the server
    socket.on('new_message', function(data) {
        const li = document.createElement('li');
        //  add message to the  a list and append to message list
        li.textContent = data.text;  
        document.getElementById('messages').appendChild(li);  
    });
});