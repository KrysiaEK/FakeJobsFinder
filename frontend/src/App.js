import * as React from "react";
import { Admin, Resource } from 'react-admin';
import jsonServerProvider from 'ra-data-json-server';

import { JobList, JobShow } from './posts';
import authProvider from './authProvider';


const dataProvider = jsonServerProvider('/api/v1');
const App = () => (
    <Admin dataProvider={dataProvider}>
        <Resource name="jobs" list={JobList} show={JobShow} />
    </Admin>
);

export default App;