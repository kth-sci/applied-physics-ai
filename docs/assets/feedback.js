/**
 * "Is this useful?" Feedback Widget
 * Stores feedback in the Hypha kth-sci/aphys-ai-feedback collection.
 */
(function() {
  const HYPHA = 'https://hypha.aicell.io';
  const FEEDBACK_COLLECTION = 'kth-sci/aphys-ai-feedback';
  const page = location.pathname.split('/').pop() || 'index.html';

  if (page === 'gallery.html' && location.hash) return;
  if (page === 'admin.html') return;

  const footer = document.querySelector('footer');
  if (!footer) return;

  const widget = document.createElement('div');
  widget.style.cssText = 'max-width:40rem;margin:3rem auto 0;padding:0 1.5rem;';
  widget.innerHTML = `
    <div style="border:1px solid #c7d2fe;border-radius:12px;padding:1.5rem;background:linear-gradient(135deg,#eef2ff,#f8fafc);text-align:center">
      <p style="font-size:0.95rem;font-weight:600;color:#0f172a;margin:0 0 0.75rem">Is this page useful?</p>
      <div id="fb-buttons" style="display:flex;gap:0.75rem;justify-content:center">
        <button id="fb-up" style="display:inline-flex;align-items:center;gap:0.4rem;padding:0.5rem 1.25rem;border:2px solid #6366f1;border-radius:8px;background:#fff;font-family:inherit;font-size:0.875rem;cursor:pointer;transition:all 0.15s;color:#6366f1;font-weight:600"
          onmouseenter="this.style.background='#6366f1';this.style.color='#fff'"
          onmouseleave="this.style.background='#fff';this.style.color='#6366f1'">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 00-3-3l-4 9v11h11.28a2 2 0 002-1.7l1.38-9a2 2 0 00-2-2.3H14zM7 22H4a2 2 0 01-2-2v-7a2 2 0 012-2h3"/></svg>
          Yes, helpful!
        </button>
        <button id="fb-down" style="display:inline-flex;align-items:center;gap:0.4rem;padding:0.5rem 1.25rem;border:2px solid #cbd5e1;border-radius:8px;background:#fff;font-family:inherit;font-size:0.875rem;cursor:pointer;transition:all 0.15s;color:#64748b;font-weight:500"
          onmouseenter="this.style.borderColor='#6366f1';this.style.color='#6366f1'"
          onmouseleave="this.style.borderColor='#cbd5e1';this.style.color='#64748b'">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 15v4a3 3 0 003 3l4-9V2H5.72a2 2 0 00-2 1.7l-1.38 9a2 2 0 002 2.3H10zM17 2h2.67A2.31 2.31 0 0122 4v7a2.31 2.31 0 01-2.33 2H17"/></svg>
          Could be better
        </button>
      </div>
      <div id="fb-comment" style="display:none;margin-top:1rem;text-align:left">
        <textarea id="fb-text" rows="3" placeholder="What could be improved? Your feedback helps us make this better..."
          style="width:100%;padding:0.6rem 0.75rem;border:2px solid #c7d2fe;border-radius:8px;font-family:inherit;font-size:0.875rem;resize:vertical;outline:none;transition:border 0.2s"
          onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#c7d2fe'"></textarea>
        <div style="text-align:right;margin-top:0.5rem">
          <button id="fb-send" style="background:#6366f1;color:#fff;font-weight:600;padding:0.5rem 1.25rem;border-radius:8px;border:none;cursor:pointer;font-size:0.875rem;font-family:inherit;transition:background 0.15s"
            onmouseenter="this.style.background='#4f46e5'" onmouseleave="this.style.background='#6366f1'">
            Send Feedback
          </button>
        </div>
      </div>
      <div id="fb-thanks" style="display:none;color:#6366f1;font-weight:600;font-size:0.95rem;padding:0.75rem 0">
        &#10003; Thank you for your feedback!
      </div>
    </div>
  `;

  footer.parentNode.insertBefore(widget, footer);

  let voted = localStorage.getItem('fb-' + page);
  if (voted) { showThanks(); return; }

  function showThanks() {
    document.getElementById('fb-buttons').style.display = 'none';
    document.getElementById('fb-comment').style.display = 'none';
    document.getElementById('fb-thanks').style.display = 'block';
  }

  async function submitFeedback(vote, comment) {
    localStorage.setItem('fb-' + page, vote);
    showThanks();
    try {
      await fetch(HYPHA + '/public/services/artifact-manager/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alias: 'fb-' + page.replace('.html','') + '-' + Date.now().toString(36),
          parent_id: FEEDBACK_COLLECTION,
          manifest: {
            name: vote === 'up' ? 'Thumbs Up: ' + page : 'Feedback: ' + page,
            page: page,
            vote: vote,
            comment: comment || '',
            timestamp: new Date().toISOString(),
            tags: ['feedback', vote, page.replace('.html','')],
          }
        })
      });
    } catch(e) { /* best-effort */ }
  }

  document.getElementById('fb-up').addEventListener('click', () => submitFeedback('up', ''));
  document.getElementById('fb-down').addEventListener('click', () => {
    document.getElementById('fb-comment').style.display = 'block';
  });
  document.getElementById('fb-send').addEventListener('click', () => {
    submitFeedback('down', document.getElementById('fb-text').value.trim());
  });
})();
