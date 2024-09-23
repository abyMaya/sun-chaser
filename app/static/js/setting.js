const edit = document.getElementById('edit');
const save = document.getElementById('save');
const usernameDisplay = document.getElementById('usernameDisplay');
const usernameInput = document.getElementById('usernameInput');

edit.addEventListener('click', () => {
  usernameInput.value = usernameDisplay.textContent;
  usernameInput.style.display = 'block';
  save.style.display = 'block';
  usernameDisplay.style.display = 'none';
  edit.style.display = 'none';
});

usernameInput.addEventListener('input', () => {
  save.disabled = usernameInput.value.trim() === '';
});

save.addEventListener('click', async () => {
  const newUsername = usernameInput.value;

  try {
    const response = await fetch('/update-username', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: newUsername}),
    });

    if (response.ok) {
        usernameDisplay.textContent = newUsername;
        usernameDisplay.style.display = 'block';
        usernameInput.style.display = 'none';
        save.style.display = 'none';
        edit.style.display = 'block';
    } else {
        alert('更新に失敗しました');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('エラーが発生しました');
  }
});

