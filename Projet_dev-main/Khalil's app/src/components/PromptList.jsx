import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, ListGroup, Form, Button } from 'react-bootstrap';
import axios from 'axios';

const PromptList = () => {
  const [prompts, setPrompts] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    axios.get('/prompts')
      .then(response => {
        setPrompts(response.data);
      })
      .catch(error => {
        console.error("Erreur lors de la récupération des prompts:", error);
      });
  }, []);

  const handleSearch = (e) => {
    setSearch(e.target.value);
  };

  return (
    <Container className="mt-4">
      <Form>
        <Form.Group controlId="search">
          <Form.Control type="text" placeholder="Rechercher un prompt" value={search} onChange={handleSearch} />
        </Form.Group>
      </Form>
      <ListGroup className="mt-4">
        {prompts.filter(prompt => prompt.content.toLowerCase().includes(search.toLowerCase())).map(prompt => (
          <ListGroup.Item key={prompt.id}>
            <Link to={`/consulter/${prompt.id}`}>{prompt.content}</Link>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </Container>
  );
};

export default PromptList;
