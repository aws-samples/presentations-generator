import { useEffect, useState } from "react";
import { Typography, Box, Container, Modal, TextField, Button } from "@mui/material";
import PresentationsTable from "../components/PresentationsTable";
import api from "../services/api";

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "80%",
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
  maxHeight: "80vh",
  overflow: "auto",
  border: "none",
};

function Presentations() {
  const [presentations, setPresentations] = useState([]);
  const [question, setInputValue] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [apiResult, setApiResult] = useState({});

  const getPresentations = () => {
    api.get("get-data").then((response) => {
      const data = response.data;
      setPresentations(data);
    });
  };

  useEffect(() => {
    // Fetch presentations data from the server
    getPresentations();
  }, []);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = () => {
     // Define the stateMachineArn here
    const stateMachineArn = 'arn:aws:states:us-east-1:537429299499:stateMachine:ppt-generator-backend-PPT-Generator-Step-Function';

    // Junta question com stateMachineArn
    const requestData = {
      question,
      stateMachineArn,
    };

    // Enviar o valor do inputValue para a API
    api.post('/gen-ppt', requestData)
    .then(response => {
      console.log('Resposta da API:', response.data);
      const sessionId = response.data.executionArn.split(':').pop();
      setApiResult({ message: 'Execução disparada com sucesso. Em breve sua apresentação estará disponível :)', sessionId });
      setShowModal(true);
    })
    .catch(error => {
      console.error('Erro ao enviar dados para a API:', error);
    });
};

  return (
    <Container
      disableGutters
      maxWidth="md"
      component="main"
      sx={{ pt: 8, pb: 6, pr: 4, pl: 4 }}
    >
      <Box display="flex" justifyContent="left">
        <Typography variant="h4">Gere sua apresentação</Typography>
      </Box>
      <Box mt={2}>
        <TextField
          label="Informe o tema de sua apresentação"
          value={question}
          onChange={handleInputChange}
          fullWidth
        />
        <Button variant="contained" onClick={handleSubmit} sx={{ mt: 2 }}>
          Enviar
        </Button>
      </Box>
      <Box mt={2}>
        <PresentationsTable presentations={presentations} onRefresh={getPresentations} />
      </Box>
      <Modal
        open={showModal}
        onClose={() => setShowModal(false)}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <Box sx={modalStyle}>
          <Typography id="modal-title" variant="h6" component="h2">
            {apiResult.message}
          </Typography>
          <Typography id="modal-description" sx={{ mt: 2 }}>
            ID da sessão: {apiResult.sessionId}
          </Typography>
        </Box>
      </Modal>
    </Container>
  );
}

export default Presentations;
