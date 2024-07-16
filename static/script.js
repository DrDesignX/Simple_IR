async function performSearch() {
    const query = document.getElementById('query-input').value;
    const response = await fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query, additional_text: '' })
    });

    const results = await response.json();
    displayResults(results);
}

function displayResults(results, currentPage = 1, itemsPerPage = 30) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
  
    // Slice the results based on current page and items per page
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, results.length);
    const paginatedResults = results.slice(startIndex, endIndex);
  
    paginatedResults.forEach(result => {
      const resultItem = document.createElement('div');
      resultItem.className = 'result-item';
  
      resultItem.innerHTML = `
      <div class="head">
        <div class="half">
          <p class="id">${result.id}</p>
          <p class="author">Published by ${result.author}</p>
        </div>
  
        <p class="similarity">Score: ${result.similarity.toFixed(4)}</p>
      </div>
      <h3>${result.title.replace('.', '')}</h3>
      <p  class="result-item-text" >${result.word.substring(0, 200)}...</p>
      <button class="btn" onclick="findSimilar('${(result.word).replace(/[^\w\d]/g, ' ')}')">Find Similar</button>
  `;
  
  
  
  
      resultsDiv.appendChild(resultItem);
    });
  
    // Add pagination controls
    const paginationContainer = document.getElementById('pagination'); // Replace with your container ID
    paginationContainer.innerHTML = '';
  
    // Check if there are more pages
    const hasPrevious = currentPage > 1;
    const hasNext = endIndex < results.length;
  
    if (hasPrevious || hasNext) {
      const buttonContainer = document.createElement('div');
      buttonContainer.className = 'pagination-buttons';
  
      if (hasPrevious) {
        const previousButton = document.createElement('button');
        previousButton.textContent = 'Previous';
        previousButton.addEventListener('click', () => displayResults(results, currentPage - 1, itemsPerPage));
        buttonContainer.appendChild(previousButton);
      }
  
      if (hasNext) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', () => displayResults(results, currentPage + 1, itemsPerPage));
        buttonContainer.appendChild(nextButton);
      }
  
      paginationContainer.appendChild(buttonContainer);
    }
  }
  

async function findSimilar(text) {
    const query = document.getElementById('query-input').value;
    const response = await fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query, additional_text: text })
    });

    const results = await response.json();
    displayResults(results);
}