import React, { useState } from 'react';
import axios from 'axios';
import './ImageGenerator.css';

const ImageGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState('');
  const [loading, setLoading] = useState(false);

  // Vite environment variable (make sure you define this in .env)
  const apiUrl = import.meta.env.VITE_API_URL;

  const generateImage = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${apiUrl}/generate-image/`, { prompt });
      setImage("data:image/png;base64," + response.data.image_base64);
    } catch (error) {
      console.error("Error generating image:", error);
      alert("Something went wrong");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h2>AI Image Generator</h2>

      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter a prompt..."
          style={{ width: '60%', padding: '10px', fontSize: '16px' }}
        />
        <button
          onClick={generateImage}
          disabled={loading}
          style={{
            marginLeft: '10px',
            padding: '10px 20px',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer',
          }}
        >
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </div>

      {image && (
        <div>
          <img src={image} alt="Generated AI" style={{ maxWidth: '100%', borderRadius: '8px' }} />
        </div>
      )}
    </div>
  );
};

export default ImageGenerator;
