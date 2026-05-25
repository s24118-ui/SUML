import {ValuationRequest, ValuationResponse} from '../types';

export async function fetchValuation(data: ValuationRequest): Promise<ValuationResponse> {
    const apiUrl = import.meta.env.VITE_API_URL;

    if (!apiUrl) {
        throw new Error("Brak adresu API. Skonfiguruj zmienną środowiskową VITE_API_URL z adresem serwera FastAPI.");
    }

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error(`Błąd serwera API (Status: ${response.status})`);
    }

    return response.json();
}
