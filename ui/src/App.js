import React, { useState, useEffect } from 'react';
import {
  Alert,
  Container,
  Typography,
  TextField,
  Button,
  TextareaAutosize,
  CircularProgress,
  FormControl,
  FormControlLabel,
  RadioGroup,
  Radio,
} from '@mui/material';
import axios from 'axios';

const API_KEY = "30cf50c0-c4b9-4b5e-be09-f971c7a36d97"
const RATE_LIMIT_MESSAGE = 'Sorry, rate limit is exceeded. Please try again later or contact sales@wordgoose.com to upgrade to an unlimited plan.'
// TODO: request entity too large error. code 413
axios.defaults.headers.common['API-KEY'] = API_KEY;

function App() {
  const [inputText, setInputText] = useState('');
  const [document, setDocument] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadErrorMessage, setUploadErrorMessage] = useState("");
  const [questionErrorMessage, setQuestionErrorMessage] = useState("");
  // const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState([]);
  const [selectedSource, setSelectedSource] = useState('RabbitMQ'); // Default selection
  const apiHost = 'http://localhost:5000'; // https://semanticgoose.onrender.com

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };


  const isSubmitDisabled = () => {
    return inputText.trim() === '' || selectedSource === null || loading || !uploaded;
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiHost}/answer`, { params: { phrase: inputText, document } });

      if (response.status === 200) {
        setAnswer(response.data.answer)
        console.log(answer)
        setLoading(false);
      } else {
        setLoading(false);
        setAnswer([]); // Update with the actual response data
      }
      setQuestionErrorMessage("")
    } catch (err) {
      setLoading(false);
      if (err.response?.status === 429) {
        setQuestionErrorMessage(RATE_LIMIT_MESSAGE)
      }
      setAnswer([]);
    }
  };


  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleFileUpload = async () => {
    if (selectedFile) {
      setUploading(true)
      const formData = new FormData();
      formData.append('file',
        selectedFile,
        selectedFile.name);
      try {
        const response = await axios.post(`${apiHost}/file`, formData);
        setUploading(false)
        setUploaded(true)
        setDocument(response.data.document)
        setUploadErrorMessage('')
      } catch (err) {
        if (err.response?.status === 429) {
          setUploadErrorMessage(RATE_LIMIT_MESSAGE)
        }
        console.log(err);
      }
    } else {
      alert('Please select a file to upload.');
    }
    setUploading(false)
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 'bold', m: 1 }}>
        Wordgoose
      </Typography>
      <Typography variant="body1" align="left" paragraph>
        Wordgoose is your document companion for simplifying the way you explore them.
      </Typography>
      <Typography variant="body1" align="left" paragraph>
        You can upload a PDF document and find relevant information to the topic you are interested in.
        After uploading the document, enter the topic you want to find. That's it. WG will run a <a href="https://en.wikipedia.org/wiki/Semantic_search">semantic search</a> and give you the most relevant results.
      </Typography>

      <div style={{ textAlign: 'center', marginTop: '16px' }}>
        <TextField type="file" onChange={handleFileChange} />
        <div style={{ textAlign: 'center', marginTop: '16px' }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleFileUpload}
            disabled={selectedFile == null}
          >
            {uploading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              'Upload'
            )}
          </Button>
        </div>
      </div>
      {uploadErrorMessage != '' ? (
        <div>
          <Alert severity="error">{uploadErrorMessage}</Alert>
        </div>
      ) : null}
      <div>
        {/* <input type="file" onChange={handleFileChange} /> */}
        {/* <button onClick={handleFileUpload}>Upload</button> */}
        {selectedFile && <p>Selected File: {selectedFile.name}</p>}
      </div>

      <TextField
        fullWidth
        variant="outlined"
        label="Question/ topic"
        value={inputText}
        onChange={handleInputChange}
        onKeyPress={(e) => e.key === 'Enter' && !isSubmitDisabled() && handleSubmit()}
        style={{ textAlign: 'center', marginTop: '16px' }}
      />
      <div style={{ textAlign: 'center', marginTop: '16px' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={isSubmitDisabled()}
        >
          {loading ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            'Ask'
          )}
        </Button>
      </div>
      {questionErrorMessage != '' ? (
        <div>
          <Alert severity="error">{questionErrorMessage}</Alert>
        </div>
      ) : null}
      {answer.length === 0 ? (
        <div style={{ textAlign: 'center', marginTop: '16px' }}>
          {/* <CircularProgress /> */}
        </div>
      ) : (
        answer.map(a => {
          return <TextareaAutosize
            rowsmin={10}
            style={{ width: '100%', marginTop: '16px' }}
            placeholder=""
            value={a.phrase}
            readOnly
          />
        })
        // <p>"hi"</p>

      )}
    </Container>
  );
}

export default App;
