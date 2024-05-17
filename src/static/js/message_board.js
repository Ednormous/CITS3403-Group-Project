// // // this Js doc doc handles the client-side for the message board and communicates to the backend server and database/

// Waits for the entire documnet to load before going on to execute the script
document.addEventListener('DOMContentLoaded', () => {
    // Establishes websocket connection
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    // references to form fields and page elements
    const messageForm = document.getElementById('message-board-form');
    const messageInput = document.getElementById('message-board-input');
    const messageLabelInput = document.getElementById('message-label-input');
    const parentIdInput = document.getElementById('message-board-parent-id');
    const unitCode = document.getElementById('unitCode').textContent;

    // New message function
    function sendMessage(text, parentId = null, label, unitCode) {
        socket.emit('post_message', { text: text, parent_id: parentId, message_label: label, unitCode: unitCode });
    }
    // Delete message function
    function deleteMessage(messageId) {
        socket.emit('delete_message', { message_id: messageId });
    }
    // Submit event handler for the message
    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        // get values and trim white space
        const text = messageInput.value.trim();
        const label = messageLabelInput.value.trim();
        const parentId = parentIdInput.value;
        // check is input is empty
        if (text !== '') {
            // send message and clear variables
            sendMessage(text, parentId || null, label, unitCode);
            messageInput.value = '';
            messageLabelInput.value = '';
            parentIdInput.value = '';
            // This is an attempt to refresh the page after the reply is posted to fix the reply issue
            setTimeout(() => {
                window.location.reload();
            },500);
        }
    });

    // Event handler for reply and delete
    document.getElementById('messages').addEventListener('click', (event) => {
        // If reply 
        if (event.target.classList.contains('reply-btn')) {
            const parentId = event.target.getAttribute('data-message-id');
            const replyForm = document.createElement('form');
            replyForm.className = 'reply-form';
            const replyInput = document.createElement('input');
            replyInput.type = 'text';
            replyInput.className = 'reply-input';
            replyInput.placeholder = 'Enter your reply here...';
            const sendButton = document.createElement('button');
            sendButton.type = 'submit';
            sendButton.textContent = 'Send';

            replyForm.appendChild(replyInput);
            replyForm.appendChild(sendButton);
            event.target.after(replyForm);

            replyInput.focus();

            replyForm.onsubmit = (e) => {
                e.preventDefault();
                const replyText = replyInput.value.trim();
                if (replyText !== '') {
                    sendMessage(replyText, parentId, '', unitCode);
                    replyForm.remove();

                }
            };
        }

        // if Delete clicked then delete
        if (event.target.classList.contains('delete-btn')) {
            const messageId = event.target.getAttribute('data-message-id');
            deleteMessage(messageId);

        }
    });
    // event handler for recieving new message
    socket.on('new_message', (data) => {
        const messageList = document.getElementById('messages');
        const messageItem = document.createElement('li');
        messageItem.setAttribute('data-message-id', data.message_id);
        messageItem.classList.add('message-item');

        // if label then add to message
        if (data.label && data.label.trim() !== '') {
            const labelElement = document.createElement('div');
            labelElement.textContent = data.label;
            labelElement.className = 'message-label';
            messageItem.appendChild(labelElement);

        }

        // add content and username
        const contentElement = document.createElement('div');
        // contentElement.textContent = `${data.username}: ${data.text}`;
        contentElement.className = 'message-content';
        // messageItem.appendChild(contentElement);
        messageItem.innerHTML = `${data.username}: ${data.text}`;


    

        // add delete button only if username matches current user or site admin
        if (data.user_id == current_user_id || current_user_role === 'admin') {
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.className = 'delete-btn';
            deleteButton.setAttribute('data-message-id', data.message_id);
            messageItem.appendChild(deleteButton);
        }
        

        // Append to message as reply to parent message if it exists else to main
        if (data.parent_id) {
            const parentMessage = document.querySelector(`[data-message-id='${data.parent_id}'] .replies`);
            if (parentMessage) {
                parentMessage.appendChild(messageItem);


            }
        } else {
            //  empty list for replies
            const repliesList = document.createElement('ul');
            repliesList.className = 'replies';
            messageItem.appendChild(repliesList);

            const replyButton = document.createElement('button');
            replyButton.textContent = 'Reply';
            replyButton.className = 'reply-btn';
            replyButton.setAttribute('data-message-id', data.message_id);
            messageItem.appendChild(replyButton);
            messageList.appendChild(messageItem);


        }
    });
    //  Delete event
    socket.on('message_deleted', (data) => {
        // locate message by message id and remove it from the dom
        const messageItem = document.querySelector(`[data-message-id='${data.message_id}']`);
        if (messageItem) {
            messageItem.remove();
        }
    });
    //  Display error messages in alert box
    socket.on('error', (data) => {
        alert(data.error);
    });
});

// This project includes code generated with the assistance of git-hub copilot
// This project includes code generated with the assistance of OpenAI's ChatGPT.
// Consulted ChatGPT for help with implementing the edit and delete features, WebSocket event handling, and ensuring that users can only edit or delete their own messages, except for administrators who can delete any message.

// **Citation:**
// ChatGPT, OpenAI. “Flask WebSocket Message Board Code Assistance.” ChatGPT, OpenAI, 2024.
