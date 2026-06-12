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
        let detail = `Błąd serwera API (Status: ${response.status})`;
        try {
            const body = await response.json();
            if (typeof body.detail === 'string') {
                detail = body.detail;
            }
        } catch {
            // ignore JSON parse errors
        }
        throw new Error(detail);
    }

    return response.json();
}
