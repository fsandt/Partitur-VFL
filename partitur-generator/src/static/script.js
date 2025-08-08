document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.instrument-list input[type="checkbox"]').forEach(input => {
    input.addEventListener('change', () => {
      input.parentElement.classList.toggle('selected', input.checked);
    });
  });
});
