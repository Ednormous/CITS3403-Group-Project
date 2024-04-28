// this Js doc is the client-side for the message board/


document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Function to send new message or reply to the server
    function sendMessage(text, parentId = null) {
        socket.emit('post_message', { text: text, parent_id: parentId });
    }

    // Listener for new message events emitted from the server
    socket.on('new_message', function(data) {
        const messageList = document.getElementById('messages');
        const li = document.createElement('li');
        li.textContent = `${data.user.username}: ${data.text}`; // Assuming `user` object contains `username`
        li.setAttribute('data-message-id', data.message_id);

        if (data.parent_id) {
            let parentMessageLi = document.querySelector(`li[data-message-id="${data.parent_id}"]`);
            if (!parentMessageLi) {
                console.error(`Parent message with id ${data.parent_id} not found!`);
                return;
            }
            
            let repliesDiv = parentMessageLi.querySelector('.replies');
            if (!repliesDiv) {
                repliesDiv = document.createElement('div');
                repliesDiv.className = 'replies';
                parentMessageLi.appendChild(repliesDiv);
            }
            
            let replyContainer = document.createElement('div');
            replyContainer.className = 'message-container';
            replyContainer.appendChild(li);
            repliesDiv.appendChild(replyContainer);
        } else {
            messageList.appendChild(li);
            
            let repliesDiv = document.createElement('div');
            repliesDiv.className = 'replies';
            li.appendChild(repliesDiv);
            
            let replyButton = document.createElement('button');
            replyButton.textContent = 'Reply';
            replyButton.className = 'reply-btn';
            replyButton.setAttribute('data-message-id', data.message_id);
            li.appendChild(replyButton);
        }
    });

    document.getElementById('messages').addEventListener('click', function(event) {
        if (event.target.classList.contains('reply-btn')) {
            const existingReplyForms = document.querySelectorAll('.reply-form');
            existingReplyForms.forEach(form => form.remove());

            const replyForm = document.createElement('form');
            replyForm.className = 'reply-form';
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'reply-input';
            input.placeholder = 'Enter your reply here...';
            const sendButton = document.createElement('button');
            sendButton.type = 'submit';
            sendButton.textContent = 'Send';

            replyForm.appendChild(input);
            replyForm.appendChild(sendButton);
            event.target.after(replyForm);

            const parentId = event.target.getAttribute('data-message-id');
            replyForm.dataset.parentId = parentId;

            input.focus();

            replyForm.onsubmit = function(e) {
                e.preventDefault();
                if (input.value.length > 0) {
                    sendMessage(input.value, parentId);
                    replyForm.remove(); // Remove the reply form after sending the message
                }
            };
        }
    });

    // Event listener for the message board form submission
    document.getElementById('message-board-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevents the default form submission which reloads the page
        const messageInput = document.getElementById('message-board-input'); // Gets the message input element
        const messageText = messageInput.value; // Extracts the text from the input
        const parentId = document.getElementById('message-board-parent-id').value || null; // Gets the parent ID if any

        // Check if the message is not just empty or spaces
        if (messageText.trim()) {
            sendMessage(messageText, parentId); // Sends the message using the existing sendMessage function
            messageInput.value = ''; // Clears the input after sending
        }
    });
});


// OpenAI. (2024). ChatGPT (4) [Large language model]. https://chat.openai.com