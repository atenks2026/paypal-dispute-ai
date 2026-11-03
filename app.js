const form = document.getElementById('disputeForm');
const result = document.getElementById('result');
const appealText = document.getElementById('appealText');
const error = document.getElementById('error');
const backendStatus = document.getElementById('backendStatus');

// Backend URL (override via environment or defaults to localhost for dev)
const BACKEND_URL = window.APP_BACKEND_URL || 'http://localhost:5000';

let lastSource = 'static'; // 'llm' | 'fallback' | 'static'

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  error.style.display = 'none';
  result.style.display = 'none';

  const disputeType = document.getElementById('disputeType').value;
  const transactionDetails = document.getElementById('transactionDetails').value;
  const evidence = document.getElementById('evidence').value;

  const btn = form.querySelector('button[type="submit"]');
  const originalText = btn.textContent;
  btn.textContent = 'Memproses AI...';
  btn.disabled = true;

  try {
    let appeal = '';
    lastSource = 'static';

    // Coba backend API dulu (LLM via NVIDIA NIM + PayPal send-message)
    try {
      const resp = await fetch(`${BACKEND_URL}/api/disputes/demo-001/appeal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dispute_type: disputeType,
          transaction_details: transactionDetails,
          evidence: evidence
        })
      });
      if (resp.ok) {
        const data = await resp.json();
        appeal = data.letter || '';
        lastSource = data.letter_source || 'fallback';
      } else {
        throw new Error(`Backend HTTP ${resp.status}`);
      }
    } catch (backendErr) {
      // Backend tidak tersedia → gunakan static template
      appeal = generateAppeal(disputeType, transactionDetails, evidence);
      lastSource = 'static';
    }

    appealText.value = appeal;
    result.style.display = 'block';
    result.scrollIntoView({ behavior: 'smooth' });

    // Tampilkan sumber surat di bawah result
    const sourceNote = document.getElementById('sourceNote') || createSourceNote();
    sourceNote.textContent = `Sumber surat: ${getSourceLabel(lastSource)}`;
    sourceNote.style.display = 'block';

  } catch (err) {
    error.textContent = 'Gagal generate surat: ' + err.message;
    error.style.display = 'block';
  } finally {
    btn.textContent = originalText;
    btn.disabled = false;
  }
});

function generateAppeal(type, details, evidence) {
  const typeLabels = {
    'SNAD': 'Significantly Not As Described',
    'INR': 'Item Not Received',
    'UAT': 'Unauthorized Transaction'
  };

  return `PayPal Resolution Center\n\nSubject: Dispute Appeal - ${typeLabels[type]}\n\nDear PayPal Team,\n\nI am writing to formally appeal the decision regarding my dispute case involving the following transaction:\n\nTransaction Details: ${details}\nDispute Type: ${typeLabels[type]}\n\nEvidence Submitted:\n${evidence}\n\nI believe the previous decision was made without full consideration of the evidence provided. I kindly request a re-review of my case with the attached documentation.\n\nThank you for your time and assistance.\n\nSincerely,\nPayPal Dispute AI User\n${new Date().toLocaleDateString()}`;
}

function createSourceNote() {
  const note = document.createElement('div');
  note.id = 'sourceNote';
  note.style.fontSize = '12px';
  note.style.color = '#666';
  note.style.marginTop = '8px';
  note.style.fontStyle = 'italic';
  result.appendChild(note);
  return note;
}

function getSourceLabel(source) {
  const labels = {
    'llm': 'AI (NVIDIA NIM) — surat digenerate oleh LLM',
    'fallback': 'Template statis (fallback, NIM tidak tersedia)',
    'static': 'Template statis (backend tidak tersedia)'
  };
  return labels[source] || labels['static'];
}

function copyAppeal() {
  appealText.select();
  document.execCommand('copy');
  alert('Surat appeal sudah disalin ke clipboard.');
}

function downloadAppeal() {
  const blob = new Blob([appealText.value], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'surat-appeal-paypal.txt';
  a.click();
  URL.revokeObjectURL(url);
}
