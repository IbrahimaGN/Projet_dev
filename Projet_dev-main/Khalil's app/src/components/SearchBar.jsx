import React, { useState } from 'react';
import axios from 'axios';
import { Form, Button, Container, ListGroup } from 'react-bootstrap';

const SearchBar = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = () => {
        axios.get(`http://localhost:5000/search?query=${query}`)
            .then(response => {
                setResults(response.data);
            })
            .catch(error => {
                console.error('There was an error searching for prompts!', error);
            });
    };

    return (
        <Container>
            <Form className="my-4">
                <Form.Group controlId="formSearch">
                    <Form.Control
                        type="text"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        placeholder="Search for prompts..."
                    />
                </Form.Group>
                <Button variant="primary" onClick={handleSearch} className="mt-2">
                    Search
                </Button>
            </Form>
            <ListGroup>
                {results.map(result => (
                    <ListGroup.Item key={result.id}>{result.content}</ListGroup.Item>
                ))}
            </ListGroup>
        </Container>
    );
};

export default SearchBar;
