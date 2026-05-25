import {useState} from 'react';
import {ValuationRequest, ValuationResponse} from '../types';
import {fetchValuation} from '../api/valuation';

export function useValuation() {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [result, setResult] = useState<ValuationResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const submit = async (data: ValuationRequest) => {
        setIsSubmitting(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetchValuation(data);
            setResult(response);
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Błąd podczas łączenia z FastAPI.");
        } finally {
            setIsSubmitting(false);
        }
    };

    return {isSubmitting, result, error, submit};
}
