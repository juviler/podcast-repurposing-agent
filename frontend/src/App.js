import React, { useState, useRef } from 'react';
import {
  Box,
  Button,
  Input,
  InputGroup,
  InputRightElement,
  Textarea,
  Select,
  Heading,
  Text,
  VStack,
  Skeleton,
  Stack
} from '@chakra-ui/react';

// Main App Component
function App() {
  // State variables
  const [transcript, setTranscript] = useState('');
  const [file, setFile] = useState(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [taskType, setTaskType] = useState('blog_outline');
  const [generatedContent, setGeneratedContent] = useState('');
  const [warningMessage, setWarningMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTranscriptLoading, setIsTranscriptLoading] = useState(false);

  const generatedRef = useRef();

  // Handles local file upload (.txt, .pdf, .docx)
  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    setTranscript('');
    setGeneratedContent('');
    setIsTranscriptLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);

      const res = await fetch('https://podcast-repurposing-agent.onrender.com/transcript', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      if (data.transcript) {
        setTranscript(data.transcript);
      } else {
        alert('Error: ' + (data.error || 'Unknown'));
      }
    } catch (err) {
      console.error(err);
      alert('An error occurred while fetching the transcript.');
    } finally {
      setIsTranscriptLoading(false);
    }
  };

  // Handles transcript generation from a YouTube URL
  const handleGetTranscript = async () => {
    setTranscript('');
    setGeneratedContent('');
    setIsTranscriptLoading(true);

    try {
      const res = await fetch('https://podcast-repurposing-agent.onrender.com/transcript-from-youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: youtubeUrl }),
      });

      const data = await res.json();
      if (data.transcript) {
        setTranscript(data.transcript);
      } else {
        alert('Error: ' + (data.error || 'Unknown'));
      }
    } catch (err) {
      console.error(err);
      alert('An error occurred while fetching the transcript.');
    } finally {
      setIsTranscriptLoading(false);
    }
  };

  // Sends the transcript and task type to the backend to generate output
  const handleGenerateContent = async () => {
    if (!transcript) {
      alert('No transcript available.');
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch('https://podcast-repurposing-agent.onrender.com/generate-content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript, task_type: taskType }),
      });

      const data = await res.json();

      if (data.result) {
        setGeneratedContent(data.result);
        setWarningMessage(data.warning || '');
      } else {
        alert('Error: ' + (data.error || 'Unknown'));
      }
    } catch (err) {
      console.error(err);
      alert('An error occurred while generating content.');
    } finally {
      setIsLoading(false);
    }
  };

  // Copies generated content to clipboard
  const handleCopy = () => {
    if (generatedRef.current) {
      generatedRef.current.select();
      navigator.clipboard.writeText(generatedRef.current.value);
    }
  };

  // App layout
  return (
    <Box maxW="800px" mx="auto" p={6}>
      <Heading mb={6}>Podcast Repurposing Agent</Heading>

      {/* Upload Section (File or YouTube) */}
      <VStack align="start" spacing={4} mb={8}>
        <Heading size="md">1. Upload Transcript</Heading>

        <Stack direction="row" spacing={4} align="center">
          <FileUploadButton onFileSelect={handleFileUpload} />
          <Text position="relative" whiteSpace="nowrap">or</Text>
          <InputGroup>
            <Input
              placeholder="Paste YouTube URL"
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
            />
            <InputRightElement width="6rem">
              <Button
                h="1.75rem"
                size="sm"
                colorScheme="orange"
                onClick={handleGetTranscript}
                isDisabled={!youtubeUrl.trim() && !file}
              >
                Get
              </Button>
            </InputRightElement>
          </InputGroup>
        </Stack>
      </VStack>

      {/* Transcript Display */}
      <VStack align="start" spacing={4} mb={8}>
        {isTranscriptLoading ? (
          <Skeleton height="200px" width="100%" />
        ) : (
          <Textarea
            value={transcript}
            readOnly
            placeholder="Transcript will appear here"
            resize="none"
            height="200px"
          />
        )}
      </VStack>

      {/* Task Selector and Generator */}
      <VStack align="start" spacing={4} mb={8}>
        <Heading size="md">2. Choose Output Type</Heading>
        <Select
          value={taskType}
          onChange={(e) => setTaskType(e.target.value)}
          isDisabled={!transcript}
        >
          <option value="">-- Choose an output --</option>
          <option value="blog_outline">Blog Outline</option>
          <option value="newsletter_blurb">Newsletter Blurb</option>
          <option value="shorts_script">YouTube Shorts Script</option>
          <option value="quote_finder">Top Quotes</option>
          <option value="linkedin_post">LinkedIn Post</option>
          <option value="internal_summary">Internal Summary</option>
        </Select>
        <Button
          colorScheme="orange"
          onClick={handleGenerateContent}
          isDisabled={transcript.trim() === ''}
        >
          Generate Content
        </Button>
      </VStack>

      {/* Generated Output Viewer */}
      <VStack align="start" spacing={2} mb={8}>
        <Heading size="md">3. Generated Output</Heading>

        <Box position="relative" width="100%">
          {generatedContent && (
            <Button
              size="sm"
              colorScheme="gray"
              position="absolute"
              top="8px"
              right="8px"
              zIndex="1"
              onClick={handleCopy}
            >
              Copy
            </Button>
          )}

          {isLoading ? (
            <Skeleton height="500px" width="100%" />
          ) : (
            <Textarea
              ref={generatedRef}
              value={generatedContent}
              readOnly
              placeholder="Generated content will appear here"
              resize="none"
              height="500px"
              pr="80px"
            />
          )}
        </Box>

        {/* Optional warning (e.g. model limits) */}
        {warningMessage && (
          <Text color="orange.500" fontWeight="semibold">
            ⚠️ {warningMessage}
          </Text>
        )}
      </VStack>
    </Box>
  );
}

// File upload helper component
function FileUploadButton({ onFileSelect, fileName }) {
  const inputRef = useRef();

  return (
    <Box>
      <input
        type="file"
        ref={inputRef}
        style={{ display: 'none' }}
        onChange={onFileSelect}
      />
      <Button onClick={() => inputRef.current.click()} colorScheme="orange">
        Upload File
      </Button>
      {fileName && (
        <Text mt={1} fontSize="sm" color="gray.600">
          {fileName}
        </Text>
      )}
    </Box>
  );
}

export default App;
