/**
 * Page View Counter
 * Uses Hypha artifact view_count as a persistent, never-resetting counter.
 * Reading an artifact with silent=false increments its view_count.
 */
(function() {
  const HYPHA = 'https://hypha.aicell.io';
  const page = (location.pathname.split('/').pop() || 'index.html').replace('.html', '');
  const artifactId = 'kth-sci/views-' + page;

  // Find the footer and insert the counter
  const footer = document.querySelector('footer');
  if (!footer) return;

  // Create counter element
  const counter = document.createElement('p');
  counter.style.cssText = 'margin-top:0.5rem;font-size:0.72rem;color:#64748b;display:flex;align-items:center;justify-content:center;gap:0.35rem;';
  counter.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="opacity:0.5"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg><span id="view-count">...</span> views';
  footer.appendChild(counter);

  // Read artifact (silent=false → increments view_count) and display
  fetch(HYPHA + '/' + artifactId.split('/')[0] + '/artifacts/' + artifactId.split('/')[1] + '?silent=false')
    .then(r => r.json())
    .then(data => {
      const count = Math.round(data.view_count || 0);
      document.getElementById('view-count').textContent = count.toLocaleString();
    })
    .catch(() => {
      counter.style.display = 'none';
    });
})();
