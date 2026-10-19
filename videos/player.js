(() => {
  const film = document.querySelector('[data-film]');
  if (!film) return;
  const video = film.querySelector('video');
  const start = film.querySelector('[data-film-start]');
  const status = film.querySelector('[data-film-status]');
  let timeout;
  let attempt = 0;
  const state = (name, message = '') => {
    film.dataset.state = name;
    status.textContent = message;
    film.setAttribute('aria-busy', String(name === 'loading'));
    start.textContent = name === 'error' ? '重试播放' : '播放宣传片';
  };
  const wait = () => {
    clearTimeout(timeout);
    state('loading', '视频加载中…');
    timeout = setTimeout(() => {
      video.pause();
      state('error', '视频加载较慢，请重试，或使用下方的直接观看入口。');
    }, 20000);
  };
  const fail = () => {
    clearTimeout(timeout);
    video.controls = false;
    state('error', '暂时无法播放，请重试，或使用下方的直接观看入口。');
  };
  const play = () => {
    const currentAttempt = ++attempt;
    video.controls = true;
    film.scrollIntoView({block: 'center', behavior: 'instant'});
    if (video.error || video.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) video.load();
    wait();
    video.play().catch(() => { if (currentAttempt === attempt) fail(); });
  };
  document.querySelectorAll('[data-play-film]').forEach(button => button.addEventListener('click', event => {
    event.preventDefault();
    play();
  }));
  video.addEventListener('playing', () => { clearTimeout(timeout); state('playing'); });
  video.addEventListener('waiting', wait);
  video.addEventListener('pause', () => {
    clearTimeout(timeout);
    if (film.dataset.state !== 'error') state('paused');
  });
  video.addEventListener('ended', () => { clearTimeout(timeout); state('ended'); start.textContent = '重新播放'; });
  video.addEventListener('error', fail);
  video.controls = false;
  state('idle');
})();
