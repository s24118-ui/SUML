import {Header} from './components/Header';
import {Footer} from './components/Footer';
import {ValuationForm} from './components/ValuationForm';
import {OutputPanel} from './components/OutputPanel';
import {useValuation} from './hooks/useValuation';

export default function App() {
    const {isSubmitting, result, error, submit} = useValuation();

    return (
        <div
            className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans overflow-auto lg:overflow-hidden">
            <Header/>

            <main className="mx-auto flex-1 flex flex-col px-6 lg:px-12 py-10 gap-10 lg:overflow-hidden">
                <ValuationForm isSubmitting={isSubmitting} onSubmit={submit}/>
                <OutputPanel isSubmitting={isSubmitting} error={error} result={result}/>
            </main>

            <Footer/>
        </div>
    );
}
