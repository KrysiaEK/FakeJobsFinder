import React, { useState } from 'react';
import { TextInput, useNotify, useDataProvider } from 'react-admin';
import { TextField, Button , useFormControl } from '@mui/material';

const SendEmailButton = (props) => {
  const [email, setEmail] = useState("");
  const [body, setBody] = useState("");
  const dataProvider = useDataProvider();
  const notify = useNotify();
  
  const handleClick = () => {
    dataProvider.create('emails', { data: { email, body }})
      .then(() => {
        notify('Email sent successfully');
        setEmail("");
        setBody("");
      })
      .catch((error) => {
        notify('Error: email not sent', 'warning');
      });
  };

  return (
    <div>
      <TextInput source="email" value={""} onChange={(e) => setEmail(e.target.value)} label="Email" />
      <TextField
        id="outlined-multiline-static"
        label="Body"
        multiline
        rows={4}
        value={"body"}
        onChange={(e) => setBody(e.target.value)}
        variant="outlined"
        fullWidth
      />
      <Button label="Send" onClick={handleClick}>Send</Button>
    </div>
  );
};

export default SendEmailButton;
