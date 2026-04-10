document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analyze-form');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');
    const inputSection = document.querySelector('.input-section');
    const approveBtn = document.getElementById('approve-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const url = document.getElementById('url').value;
        const brd = document.getElementById('brd').value;

        // UI State: Loading
        inputSection.style.opacity = '0.5';
        inputSection.style.pointerEvents = 'none';
        resultsSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url, brd })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to analyze logic');
            }

            const resData = await response.json();
            const data = resData.data;

            // Populate Results
            document.getElementById('res-purpose').textContent = data.system_purpose;

            const ulPersonas = document.getElementById('res-personas');
            ulPersonas.innerHTML = '';
            data.user_personas.forEach(p => {
                const li = document.createElement('li');
                li.textContent = p;
                ulPersonas.appendChild(li);
            });

            const ulPaths = document.getElementById('res-paths');
            ulPaths.innerHTML = '';
            data.critical_business_paths.forEach(p => {
                const li = document.createElement('li');
                li.textContent = p;
                ulPaths.appendChild(li);
            });

            const ulLogic = document.getElementById('res-logic');
            ulLogic.innerHTML = '';
            data.assumed_logic.forEach(l => {
                const li = document.createElement('li');
                li.textContent = l;
                ulLogic.appendChild(li);
            });

            // UI State: Complete
            loadingSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');

            // Re-enable inputs but keep focus on results
            inputSection.style.opacity = '1';
            inputSection.style.pointerEvents = 'all';

        } catch (error) {
            console.error(error);
            alert('Error: ' + error.message);
            loadingSection.classList.add('hidden');
            inputSection.style.opacity = '1';
            inputSection.style.pointerEvents = 'all';
        }
    });

    approveBtn.addEventListener('click', () => {
        alert('Logic Approved! The system will now begin writing test cases and initiating the Playwright Test Execution Agents...');
        // In Step 2, this would transition to the actual execution phase UI.
    });
});
