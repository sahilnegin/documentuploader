import React, { useState } from 'react';
import './DocumentUploaderAndChat.css';
function DocumentUploaderAndChat() {
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [prompt, setPrompt] = useState('');

  const handleDocumentChange = (e) => {
    const file = e.target.files[0];
    setSelectedDocument(file);
  };

  const handlePromptChange = (e) => {
    setPrompt(e.target.value);
  };

  const handleUpload = () => {
    // Implement your document upload logic here, e.g., send the selectedDocument to a server.
    if (selectedDocument) {
      alert(`Document "${selectedDocument.name}" uploaded successfully!`);
    } else {
      alert('Please select a document before uploading.');
    }
  };

  const handleStartChat = () => {
    // Implement your chat initiation logic here, using the 'prompt' value.
    alert(`Starting chat with prompt: "${prompt}"`);
  };

  return (
<div>
  <div>
    
    <h2>Document Uploader</h2>
    <label htmlFor="fileInput" className="file-label">Choose File</label>
    <input
  type="file"
  id="fileInput"
  accept=".pdf, .doc, .docx"
  onChange={handleDocumentChange}
  style={{ display: 'none' }}
  multiple  
/>
    <button onClick={handleUpload}>Upload Document</button>
  </div>
  <div class="chat-bar">
   
    <input
      type="text"
      placeholder="Enter a prompt..."
      value={prompt}
      onChange={handlePromptChange}
    />
<button onClick={handleStartChat} class="icon-button">
  <img src="icon.png" alt="Chat Icon" height="25px" class="icon" />
</button>



  </div>
  <div class="para">
    <p>You can Chat with your documents here </p>
  </div>
</div>

  );
}

export default DocumentUploaderAndChat;
