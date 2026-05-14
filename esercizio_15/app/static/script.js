// Live search script with debounce and safe encoding
(function(){
  const input = document.getElementById('search');
  const resultsList = document.getElementById('risultati');
  let timeout = null;

  function renderResults(items){
    resultsList.innerHTML = '';
    if(!items || items.length === 0) return;
    items.forEach(item => {
      const li = document.createElement('li');
      li.textContent = (item.nome || '') + (item.provincia ? ' (' + item.provincia + ')' : '');
      resultsList.appendChild(li);
    });
  }

  function fetchResults(q){
    // If empty query, clear results and return
    if(!q || q.trim() === ''){
      renderResults([]);
      return;
    }

    fetch('/cerca?q=' + encodeURIComponent(q))
      .then(r => {
        if(!r.ok) throw new Error('network response was not ok');
        return r.json();
      })
      .then(data => renderResults(data))
      .catch(err => {
        console.error('fetch error', err);
      });
  }

  // debounce on input events
  input.addEventListener('input', function(){
    clearTimeout(timeout);
    const q = this.value;
    timeout = setTimeout(() => fetchResults(q), 200);
  });
})();
