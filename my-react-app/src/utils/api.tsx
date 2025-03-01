import axios from 'axios';



export default function api() {

    const myAxios = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 20000,
        headers: {
            "Content-Type": "application/json",
        },
    });
    
    return {
        getReflectSummary: async () => {
            return myAxios.get('/reflect');
        },

        getStartPrompt: async () => {
            return myAxios.get('/start');
        },

        getFurtherPrompt: async () => {
            return myAxios.get('/further');
        },
        testapi: async () => {
            return myAxios.get('/test-ai');
        },
    };
}