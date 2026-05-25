import {AnimatePresence} from 'motion/react';
import {ValuationResponse} from '../types';
import {EmptyState} from './EmptyState';
import {ErrorDisplay} from './ErrorDisplay';
import {ResultDisplay} from './ResultDisplay';

interface OutputPanelProps {
    isSubmitting: boolean;
    error: string | null;
    result: ValuationResponse | null;
}

export function OutputPanel({isSubmitting, error, result}: OutputPanelProps) {
    return (
        <section className="flex-1 flex flex-col gap-6 lg:overflow-y-auto">
            <AnimatePresence mode="wait">
                {error && <ErrorDisplay message={error}/>}
                {!error && !result && !isSubmitting && <EmptyState/>}
                {result && !error && <ResultDisplay result={result}/>}
            </AnimatePresence>
        </section>
    );
}
