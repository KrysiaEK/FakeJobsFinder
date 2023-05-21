import * as React from "react";
import { fetchUtils, useDataProvider, useCreate, List, Datagrid, TextField, Show,SaveButton, SimpleShowLayout, Button, useRecordContext, Create, FunctionField, Edit, SimpleForm, ReferenceInput, SelectInput, TextInput, required  } from 'react-admin';
import { CardActions } from '@mui/material';
import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import html2pdf from 'html2pdf.js';

const JobViewImageButton = () => {
  const record = useRecordContext();
  const handleImageClick = () => {
    const imageUrl = `/api/v1/jobs/${record.id}/image`; // Replace 'image' with the actual field name for the image URL
    window.open(imageUrl, "_blank");
  };

  return (
    <Button label="View website copy" onClick={handleImageClick} style={{ marginLeft: '1em' }} />
  );
};

const getScore = (record) => {
    if(record.score >= 5) {
        return <span style={{ color: 'rgb(255, 50, 50)', fontWeight: 'bold' }}>BARDZO WYSOKIE</span>;
    } else if (record.score >= 4) {
        return <span style={{ color: 'rgb(255, 50, 50)' }}>WYSOKIE</span>;
    } else if (record.score >= 3) {
        return "ŚREDNIE";
    } else if (record.score >= 2) {
        return <span style={{ color: 'rgb(100, 200, 0)' }}>NISKIE</span>;
    }
    return <span style={{ color: 'rgb(0, 255, 0)' }}>BARDZO NISKIE</span>;
};

const getNegativeKeyword = () => {
    const record = useRecordContext();
    if (record.negative_keywords) {
      return record.negative_keywords.split(";").join(", ");
    }
    return "";
};

const getPositiveKeyword = () => {
    const record = useRecordContext();
    if (record.positive_keywords) {
      return record.positive_keywords.split(";").join(", ");
    }
    return "";
};


const getNegatives = () => {
    const record = useRecordContext();
    if (record.negatives) {
      return record.negatives.split(";").join(", ");
    }
    return "";
};

const getPositives = () => {
    const record = useRecordContext();
    if (record.positives) {
      return record.positives.split(";").join(", ");
    }
    return "";
};


function convertString(str) {
    const polishChars = {
      'ą': 'a',
      'ć': 'c',
      'ę': 'e',
      'ł': 'l',
      'ń': 'n',
      'ó': 'o',
      'ś': 's',
      'ź': 'z',
      'ż': 'z'
    };
  
    const convertedStr = str.toLowerCase().replace(/[ąćęłńóśźż]/g, char => polishChars[char]);
  
    return convertedStr;
  }
  
/*
const getDescription = () => {
    const record = useRecordContext();

    // The words you want to highlight
    const positive_keywords = convertString(record.positive_keywords).split(';');
    const negative_keywords = convertString(record.negative_keywords).split(';');
    const description = convertString(record.description);

    const parts = useMemo(() => {
        let parts = [];
        let start = 0;

        while(start < description.length) {
            let index = description.length;
            let candidate = [""];
            positive_keywords.forEach(word => {
                let candidate_index = description.indexOf(word, start);
                if(word.length > 0 &&  candidate_index >= 0 && index > candidate_index) {
                    index = candidate_index;
                    candidate = [word, true]
                }
            });
            negative_keywords.forEach(word => {
                let candidate_index = description.indexOf(word, start);
                if(word.length > 0 && candidate_index >= 0 && index > candidate_index) {
                    index = candidate_index;
                    candidate = [word, false]
                }
            });
            console.log(start, index, candidate);
            if(index == description.length || candidate[0].length == 0) {
                break;
            }
            if(index != start) {
                parts.push(<>{record.description.substring(start, index)}</>)
            }

            parts.push(<span key={start} style={{ backgroundColor: candidate[1] ? 'lightgreen' : 'rgba(255, 0, 0, 0.3);' }}>{record.description.substring(index, index + candidate[0].length)}</span>);
            start = index + candidate[0].length;
        }

        if (start < description.length) {
            parts.push(<>{record.description.substring(start)}</>);
        }

        return parts;
    }, [record.description]);

    return <>{parts}</>;

    /*
    const description = useMemo(() => {
        let newDescription = record.description;

        // This will iterate over each word and wrap it in a span with the highlight class
        positive_keywords.forEach(word => {
            const regex = new RegExp(`\\b${word}\\b`, 'ig');
            newDescription = newDescription.replaceAll(regex, `<span style="background-color: rgba(0, 255, 0, 0.3);">${word}</span>`);
        });
        negative_keywords.forEach(word => {
            const regex = new RegExp(`\\b${word}\\b`, 'ig');
            newDescription = newDescription.replaceAll(regex, `<span style="background-color: rgba(255, 0, 0, 0.3);">${word}</span>`);
        });

        return newDescription;
    }, [record.description]);

    // The dangerousSetInnerHTML prop is necessary to insert HTML tags into the component
    return <span dangerouslySetInnerHTML={{ __html: description }}></span>;
};
    */

const ChartComponent = () => {
    const dataProvider = useDataProvider();
    const [data, setData] = useState([]);
    const [types, setTypes] = useState([]);
  
    useEffect(() => {
        fetch('/api/v1/jobs/stats', {headers: { 'Content-Type': 'application/json;' }})
            .then(response => {
                if (response.status < 200 || response.status >= 300) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(data => {
                setData([data[0]]);
                setTypes([data[1]]);
            });
    }, [dataProvider]);

  
    return (
<div style={{ display: 'flex' }}>
  <div style={{ flex: 1 }}>
            <BarChart
        width={500}
        height={300}
        data={data}
        margin={{
          top: 25, left: 20, bottom: 5,
        }}
      >
        <text x="250" y="30" textAnchor="middle" fontWeight="bold">
            Number of jobs
        </text>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="olx" fill="#8884d8" />
        <Bar dataKey="sprzedajemy" fill="#82ca9d" />
        <Bar dataKey="ogloszenia24" fill="#ffc658" />
      </BarChart>
      </div>
  <div style={{ flex: 1 }}>
      <BarChart
        width={500}
        height={300}
        data={types}
        margin={{
          top: 25, right: 30, bottom: 5,
        }}
      >
        <text x="250" y="30" textAnchor="middle" fontWeight="bold">
            Suspected jobs
        </text>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="group_1" fill="#00aa00" />
        <Bar dataKey="group_2" fill="#55ff55" />
        <Bar dataKey="group_3" fill="#aaaaaa" />
        <Bar dataKey="group_4" fill="#ff5555" />
        <Bar dataKey="group_5" fill="#aa0000" />
      </BarChart>
      </div></div>
    );
  };

export const JobList = (props) => (
    <div>
                <ChartComponent />
    <List {...props}>
        <Datagrid rowClick="show">
            <TextField source="id" />
            <TextField source="provider" />
            <TextField source="title" />
            <FunctionField label="Scam proability" render={getScore} />
        </Datagrid>
    </List>
    </div>
);

export const SendEmail = () => {
    const record = useRecordContext();
    const [create] = useCreate();
    const postSave = (data) => {
        create('email', { data });
    };
    let destination = '';
    if(record.provider == 'olx') {
        destination = 'kontakt@olx.pl';
    }
    if(record.provider == 'sprzedajemy') {
        destination = 'kontakt@sprzedajemy.pl';
    }
    if(record.provider == 'ogloszenia24') {
        destination = 'kontakt@ogloszenia24.pl';
    }
    let title = `Zgłoszenie ogłoszenia - ${record.title}`;
    let email = `Szanowni Państwo,

zwracam się z uprzejmą prośbą o niezwłoczne usunięcie fałszywego ogłoszenia o pracy, które zostało opublikowane na Państwa portalu.
Tytuł ogłoszenia: ${record.title}
URL ogłoszenia: ${record.url}

Ogłoszenie to jest wyraźnym naruszeniem zasad i regulaminu Państwa portalu, ponieważ zawiera nieprawdziwe informacje oraz próbuje wprowadzić w błąd potencjalnych kandydatów. Jego obecność na Państwa platformie może negatywnie wpływać na zaufanie użytkowników oraz naruszać ich bezpieczeństwo.
Zaangażowanie Państwa w eliminowanie tego typu fałszywych ogłoszeń jest niezwykle istotne dla zapewnienia uczciwości i jakości ofert pracy. Dlatego proszę o natychmiastowe usunięcie tego ogłoszenia oraz podjęcie odpowiednich działań mających na celu zapobieganie publikacji podobnych treści w przyszłości.
Dziękuję za zrozumienie i skuteczną reakcję w tej sprawie. 

Z poważaniem, 
[Twoje imię i nazwisko]`
    return (<Create style={{ border: '1px solid black' }}>
        <SimpleForm onSubmit={postSave}>
            <TextInput fullWidth source="provider" label="Email destination" defaultValue={destination} />
            <TextInput fullWidth source="title" label="Email title" defaultValue={title} />
            <TextInput fullWidth multiline source="email_text" defaultValue={email} />
        </SimpleForm>
    </Create>  
    )
}

const handleDownload = () => {
    const element = document.getElementById("main-content");
    const opt = {
        margin:       1,
        filename:     'JobOffer.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save();
}
  
export const JobShow = (props) => {
    return (
        <Show {...props}>
            <SimpleShowLayout>
                <CardActions>
                    <Button label="Mark as legit offer" style={{ marginLeft: '1em' }} />
                    <Button label="Mark as mallicius offer" style={{ marginLeft: '1em' }} />
                    <Button label="Download as PDF" onClick={handleDownload} style={{ marginLeft: '1em' }} />
                    <JobViewImageButton />
                </CardActions>
                <TextField source="title" style={{ fontWeight: 'bold' }} />
                <TextField source="url" />
                <FunctionField label="Chance of scam" render={getScore} />
                <FunctionField label="Detected negative keywords" render={getNegativeKeyword} />
                <FunctionField label="Detected positive keywords" render={getPositiveKeyword} />
                <FunctionField label="Detected negative aspects" render={getNegatives} />
                <FunctionField label="Detected positive aspects" render={getPositives} />
                <TextField source="description" style={{ whiteSpace: "pre-wrap" }} />
                <SendEmail />
            </SimpleShowLayout>
        </Show>
    );
};
