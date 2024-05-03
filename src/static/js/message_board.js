// // this Js doc is the server-side for the message board/

// listens for the document to fully load
document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // fire up the websocket connection to the server
    function sendMessage(text, parentId = null, label, unitCode) {
        socket.emit('post_message', { text: text, parent_id: parentId, message_label: label, unitCode: unitCode });
    }

    // function to emit the posting event to the server
    socket.on('new_message', function(data) {
        const messageList = document.getElementById('messages');
        const messageItem = document.createElement('li');
        messageItem.setAttribute('data-message-id', data.message_id);
    
        // Create and append message label element
        if (data.label && data.label.trim() !== '') {
            const labelElement = document.createElement('div');
            labelElement.textContent = data.label;
            labelElement.className = 'message-label'; 
            messageItem.appendChild(labelElement);
        }
    
        // Create and append the content of the message body
        const contentElement = document.createElement('div');
        contentElement.textContent = `${data.user.username}: ${data.text}`;
        contentElement.className = 'message-content'; // Style this class in your CSS for proper formatting
        messageItem.appendChild(contentElement);
    
        // add the reply button for optional reply
        const replyButton = document.createElement('button');
        replyButton.textContent = 'Reply';
        replyButton.className = 'reply-btn';
        replyButton.setAttribute('data-message-id', data.message_id);
        messageItem.appendChild(replyButton);
    
        // Append the constructed list item to the message list
        messageList.appendChild(messageItem);
    });

    // event listner for click button
    document.getElementById('messages').addEventListener('click', function(event) {
        if (event.target.classList.contains('reply-btn')) {
            const existingReplyForms = document.querySelectorAll('.reply-form');
            existingReplyForms.forEach(form => form.remove());

            // creates new form if the element is a reply
            const replyForm = document.createElement('form');
            replyForm.className = 'reply-form';
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'reply-input';
            input.placeholder = 'Enter your reply here...';
            const sendButton = document.createElement('button');
            sendButton.type = 'submit';
            sendButton.textContent = 'Send';

            // appends the input to the bottom of the form
            replyForm.appendChild(input);
            replyForm.appendChild(sendButton);
            event.target.after(replyForm);

            // saves parentid to connect to any replys to that element
            const parentId = event.target.getAttribute('data-message-id');
            replyForm.dataset.parentId = parentId;

            input.focus();

            // submitting the reply form and clear for next event
            replyForm.onsubmit = function(e) {
                e.preventDefault();
                if (input.value.trim().length > 0) {
                    sendMessage(input.value, parentId, '', document.getElementById('unitCode').innerText); // Pass empty string for label in replies
                    replyForm.remove(); 
                }
            };
        }
    });

    // listen for submtted messages
    document.getElementById('message-board-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const messageInput = document.getElementById('message-board-input');
        const messageText = messageInput.value;
        const messageLabel = document.getElementById('message-label-input').value;
        const unitCode = document.getElementById('unitCode').textContent; 
    
        // make sure message input isnt empty and makes a new message have null parent id
        if (messageText.trim()) {
            sendMessage(messageText, null, messageLabel, unitCode); 
            messageInput.value = '';
            document.getElementById('message-label-input').value = '';  
        }
    });
    
    
});