import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, ListGroup } from 'react-bootstrap';
import axios from 'axios';

const HomePage = () => {
  const [prompts, setPrompts] = useState([]);

  useEffect(() => {
    axios.get('/prompts')
      .then(response => {
        setPrompts(response.data);
      })
      .catch(error => {
        console.error("Erreur lors de la récupération des prompts:", error);
      });
  }, []);

  return (
    <Container>
      <center><h1 className="mt-4">Bienvenue sur Khalil's app</h1>
      <ListGroup className="mt-4">
        {prompts.map(prompt => (
          <ListGroup.Item key={prompt.id}>
            <Link to={`/consulter/${prompt.id}`}>{prompt.content}</Link>
          </ListGroup.Item>
        ))}
      </ListGroup></center>
    </Container>
  );
};



export default HomePage;
