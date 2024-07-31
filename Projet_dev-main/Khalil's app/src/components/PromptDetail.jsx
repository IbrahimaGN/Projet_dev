import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Button } from 'react-bootstrap';
import axios from 'axios';

const PromptDetail = () => {
  const { id } = useParams();
  const [prompt, setPrompt] = useState(null);

  useEffect(() => {
    axios.get(`/consulter/${id}`)
      .then(response => {
        setPrompt(response.data);
      })
      .catch(error => {
        console.error("Erreur lors de la récupération du prompt:", error);
      });
  }, [id]);

  const handleBuy = () => {
    axios.post(`/buy/${id}`)
      .then(response => {
        alert(response.data.msg);
      })
      .catch(error => {
        console.error("Erreur lors de l'achat du prompt:", error);
      });
  };

  if (!prompt) {
    return <p>Chargement...</p>;
  }

  return (
    <Container className="mt-4">
      <h2>Détails du Prompt</h2>
      <p>ID: {prompt.id}</p>
      <p>Contenu: {prompt.content}</p>
      <p>Prix: {prompt.price} F CFA</p>
      <Button variant="primary" onClick={handleBuy}>Acheter</Button>
    </Container>
  );
};

export default PromptDetail;
