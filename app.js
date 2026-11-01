const form = document.getElementById('disputeForm');
const result = document.getElementById('result');
const appealText = document.getElementById('appealText');
const error = document.getElementById('error');

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
    const appeal = generateAppeal(disputeType, transactionDetails, evidence);
    
    appealText.value = appeal;
    result.style.display = 'block';
    result.scrollIntoView({ behavior: 'smooth' });
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
