/* A+ MQ - the one signup form: start the free trial (default), or book a demo.

   Trial, no code: the signup server makes a personal code (30-day trial on one computer) and returns it with the trial's file key;
     the page shows the code and downloads the setup. The server also e-mails the code when e-mail is set up.
   Trial, "I already have a code" ticked: a code from the author (or from an earlier visit) unlocks the download. The file key
     comes from the signup server, or, when the server cannot be reached, from trial/keys.json (wrapped once per author code).
   The setup is published only encrypted (trial/a-plus-mq-trial.bin): it is decrypted here, its SHA-256 checked, then saved.
   Demo: the details go to the author (signup server + FormSubmit e-mail).
   A link ending in #code=AMQ-XXXX-XXXX-XXXX (the e-mail) opens the form with that code filled in.
   Made with the AAMQ repository's DevTools\TrialPack and AAMQ\Server. */
(function () {
  var f = document.getElementById('demo-form');
  if (!f) return;
  var ar = document.documentElement.lang === 'ar';
  var T = ar ? {
    nocrypto: 'المتصفح ده ما بيدعمش التحميل الآمن. جرّب Chrome أو Edge أو Firefox بنسخة حديثة.',
    bad: 'الكود ده مش صحيح أو اتلغى أو خلصت مرات تحميله. اتأكد منه، أو ابعتلنا.',
    many: 'محاولات كتير. استنى شوية وجرّب تاني.',
    already: 'اتعمل كود تجربة للإيميل ده قبل كده. دوّر عليه في الإيميل، أو علّم "معايا كود بالفعل" واكتبه.',
    trialnet: 'سيرفر التجربة مش راضي يوصل من الشبكة دي (بعض شبكات الشركات بتقفله). جرّب من شبكة تانية زي داتا الموبايل، أو ابعتلنا:',
    make: 'بنجهّز كودك...', check: 'بنتأكد من الكود...', get: 'بنحمّل الملف...', open: 'بنفك الملف...',
    net: 'التحميل ما كملش. اتأكد من النت وجرّب تاني.', hash: 'الملف وصل ناقص أو متغيّر. جرّب تاني.'
  } : {
    nocrypto: 'This browser cannot do the secure download. Please use a recent Chrome, Edge or Firefox.',
    bad: 'This code is not valid, was withdrawn or has no downloads left. Check it, or contact us.',
    many: 'Too many tries. Please wait a little and try again.',
    already: 'A trial code was already made for this e-mail. Look for it in your inbox, or tick "I already have a code" and enter it.',
    trialnet: 'The trial server cannot be reached from this network (some company networks block it). Try another network, such as mobile data, or email us:',
    make: 'Making your code...', check: 'Checking your code...', get: 'Downloading...', open: 'Unlocking the file...',
    net: 'The download did not finish. Check your connection and try again.', hash: 'The file arrived incomplete or changed. Please try again.'
  };
  var cb = document.getElementById('has-code'), box = document.getElementById('code-box'), codeRow = document.getElementById('has-code-row');
  var modes = f.querySelectorAll('[name=_mode]');
  var codeIn = f.querySelector('[name=Code]'), btn = f.querySelector('button[type=submit]');
  var er = f.querySelector('.ferr'), erMsg = er.querySelector('span'), erDefault = erMsg.textContent;
  var subj = f.querySelector('[name=_subject]'), subjDemo = subj.value;
  var api = (f.getAttribute('data-api') || '').replace(/\/+$/, ''), base = f.getAttribute('data-base') || 'trial/';
  var lastUrl = null, lastName = null;

  function isTrial() { for (var i = 0; i < modes.length; i++) if (modes[i].checked) return modes[i].value !== 'demo'; return true; }
  function withCode() { return isTrial() && cb.checked; }
  function label() { return !isTrial() ? btn.getAttribute('data-demo') : cb.checked ? btn.getAttribute('data-dl') : btn.getAttribute('data-trial'); }

  // ---- trial / demo, and the "I already have a code" box
  function mode() {
    var t = isTrial();
    codeRow.hidden = !t;
    box.hidden = !withCode();
    codeIn.required = withCode();
    btn.textContent = label();
    subj.value = t ? btn.getAttribute('data-dl-subject') : subjDemo;
    er.hidden = true;
  }
  cb.addEventListener('change', function () { mode(); if (cb.checked) codeIn.focus(); });
  for (var i = 0; i < modes.length; i++) modes[i].addEventListener('change', mode);
  // a link from the e-mail: #code=AMQ-XXXX-XXXX-XXXX
  var m = /[#&]code=([A-Za-z0-9-]{12,20})/.exec(location.hash);
  if (m) { cb.checked = true; codeIn.value = m[1].toUpperCase(); }
  mode();

  // ---- helpers
  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }
  function norm(c) { var s = (c || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); return s.indexOf('AMQ') === 0 ? s.slice(3) : s; }
  function busy(msg) { btn.disabled = true; btn.textContent = msg; }
  function fail(msg, withMail) {
    erMsg.textContent = msg || erDefault;
    er.querySelector('a').hidden = !withMail;
    er.hidden = false; btn.disabled = false; btn.textContent = label();
  }
  function show(id) { f.hidden = true; var ok = document.getElementById(id); ok.hidden = false; ok.scrollIntoView({ block: 'center' }); }
  function save() { var a = document.createElement('a'); a.href = lastUrl; a.download = lastName; document.body.appendChild(a); a.click(); a.remove(); }
  function fields() {
    var d = {};
    new FormData(f).forEach(function (v, k) { d[k] = v; });
    delete d._mode;
    if (!withCode()) delete d.Code;
    return d;
  }
  // wait: ms before giving up (a network that blocks the server can hang for a minute otherwise)
  function post(url, d, wait) {
    var o = { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(d) };
    if (wait && window.AbortController) { var ac = new AbortController(); o.signal = ac.signal; setTimeout(function () { ac.abort(); }, wait); }
    return fetch(url, o);
  }
  // the author's e-mail copy (FormSubmit): resolves true when it was accepted
  function mail(d) {
    return post(f.getAttribute('data-ajax'), d)
      .then(function (r) { return r.json().then(function (j) { return r.ok && String(j.success) !== 'false'; }); })
      .catch(function () { return false; });
  }
  // the signup server: resolves the Response, or null when there is no server or it cannot be reached
  function server(d) {
    if (!api) return Promise.resolve(null);
    return post(api + '/api/signup', d, 10000).catch(function () { return null; });
  }

  function fetchBin(url, size) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw 'net';
      if (!r.body || !r.body.getReader) return r.arrayBuffer();
      var rd = r.body.getReader(), parts = [], got = 0;
      function pump() {
        return rd.read().then(function (x) {
          if (x.done) { var all = new Uint8Array(got), o = 0; parts.forEach(function (p) { all.set(p, o); o += p.length; }); return all.buffer; }
          parts.push(x.value); got += x.value.length;
          if (size) btn.textContent = T.get + ' ' + Math.min(99, Math.round(got * 100 / (size + 32))) + '%';
          return pump();
        });
      }
      return pump();
    });
  }

  // ---- the file key: { key: CryptoKey, rel: {file, name, size, sha256}, code?, mailed? }
  function fromRelease(c, j) {
    return c.importKey('raw', b64(j.release.key), 'AES-GCM', false, ['decrypt'])
      .then(function (k) { return { key: k, rel: j.release, code: j.code, mailed: j.mailed }; });
  }
  function keyFromServer(c, d) {
    return server(d).then(function (r) {
      if (!r) throw 'net';
      if (r.status === 403) throw 'bad';
      if (r.status === 409) throw 'already';
      if (r.status === 429) throw 'many';
      if (!r.ok) throw 'net';
      return r.json();
    }).then(function (j) { return fromRelease(c, j); });
  }
  function keyFromStatic(c, n) {
    var enc = new TextEncoder(), man;
    return fetch(base + 'keys.json', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 'net'; return r.json(); })
      .then(function (mf) { man = mf; return c.digest('SHA-256', enc.encode('aamq-trial:' + n)); })
      .then(function (h) {
        var k = man.keys[hex(h).slice(0, 16)];
        if (!k) throw 'bad';
        return c.importKey('raw', enc.encode(n), 'PBKDF2', false, ['deriveKey'])
          .then(function (pw) { return c.deriveKey({ name: 'PBKDF2', salt: b64(k.s), iterations: man.iter, hash: 'SHA-256' }, pw, { name: 'AES-GCM', length: 256 }, false, ['decrypt']); })
          .then(function (kek) { return c.decrypt({ name: 'AES-GCM', iv: b64(k.i) }, kek, b64(k.k)); })
          .catch(function () { throw 'bad'; });
      })
      .then(function (raw) { return c.importKey('raw', raw, 'AES-GCM', false, ['decrypt']); })
      .then(function (k) { return { key: k, rel: man }; });
  }

  // the personal code on the "ready" card
  function showCode(code, mailed) {
    var w = document.getElementById('my-code');
    if (!w || !code) return;
    document.getElementById('my-code-v').textContent = code;
    document.getElementById('my-code-mailed').hidden = !mailed;
    w.hidden = false;
  }

  // download, decrypt, check and save the setup with a key; then the "ready" card
  function fetchAndSave(c, got) {
    busy(T.get);
    return fetchBin(base + got.rel.file, got.rel.size)
      .then(function (buf) {
        busy(T.open);
        var u = new Uint8Array(buf);
        if (String.fromCharCode(u[0], u[1], u[2], u[3]) !== 'AMQ1') throw 'hash';
        return c.decrypt({ name: 'AES-GCM', iv: u.slice(4, 16) }, got.key, u.slice(16)).catch(function () { throw 'hash'; });
      })
      .then(function (file) {
        return c.digest('SHA-256', file).then(function (h) {
          if (hex(h) !== got.rel.sha256) throw 'hash';
          var exe = /[.]exe$/i.test(got.rel.name);
          lastUrl = URL.createObjectURL(new Blob([file], { type: exe ? 'application/octet-stream' : 'application/zip' }));
          lastName = got.rel.name;
          save();
          show('trial-ok');
        });
      });
  }

  function failWith(x, trialNet) {
    if (x === 'net' && trialNet) return fail(T.trialnet, true);
    fail(x === 'bad' ? T.bad : x === 'many' ? T.many : x === 'already' ? T.already : x === 'hash' ? T.hash : T.net);
  }

  // a trial without a code: the server makes one (stage 5)
  function newTrial(d) {
    var c = window.crypto && window.crypto.subtle;
    if (!c || !window.TextEncoder) return fail(T.nocrypto);
    if (!api) return fail(T.trialnet, true);
    d.Trial = '1';
    busy(T.make);
    var got;
    keyFromServer(c, d)
      .then(function (k) {
        got = k;
        showCode(k.code, k.mailed);
        mail(d);                      // the author's e-mail copy
        return fetchAndSave(c, got);
      })
      .catch(function (x) {
        // the code was made but the download failed: show the code anyway, so it is not lost
        if (got && got.code) { showCode(got.code, got.mailed); show('trial-ok'); document.getElementById('trial-again').hidden = true; return; }
        failWith(x, true);
      });
  }

  // a trial with a code the person already has
  function download(d) {
    var c = window.crypto && window.crypto.subtle;
    if (!c || !window.TextEncoder) return fail(T.nocrypto);
    var n = norm(d.Code);
    if (n.length !== 12) return fail(T.bad);
    busy(T.check);
    // a network that blocks the server (some offices block *.workers.dev) falls back to keys.json (author codes only)
    (api ? keyFromServer(c, d).catch(function (x) { if (x === 'net') return keyFromStatic(c, n); throw x; }) : keyFromStatic(c, n))
      .then(function (k) { mail(d); return fetchAndSave(c, k); })
      .catch(function (x) { failWith(x, false); });
  }

  function demo(d) {
    busy(btn.getAttribute('data-sending'));
    Promise.all([server(d), mail(d)]).then(function (r) {
      var saved = r[0] && r[0].ok, mailed = r[1];
      if (saved || mailed) return show('demo-ok');
      // last resort: the plain FormSubmit post (it shows its own page and comes back to #demo)
      try { HTMLFormElement.prototype.submit.call(f); } catch (x) { fail(null, true); }
    });
  }

  f.addEventListener('submit', function (e) {
    if (!window.fetch) return;           // very old browser: the plain form post to FormSubmit
    e.preventDefault();
    er.hidden = true;
    if (!f.reportValidity()) return;
    var d = fields();
    if (isTrial()) {
      delete d._honey;                   // autofill can fill the trap; the server limits trials per e-mail and per visitor
      return withCode() ? download(d) : newTrial(d);
    }
    if (d._honey) return show('demo-ok');
    demo(d);
  });

  var again = document.getElementById('trial-again');
  if (again) again.addEventListener('click', function (e) { e.preventDefault(); if (lastUrl) save(); });
  var copy = document.getElementById('copy-code');
  if (copy) copy.addEventListener('click', function () {
    var v = document.getElementById('my-code-v').textContent;
    var done = function () { copy.textContent = copy.getAttribute('data-done'); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(done, function () { });
    else { var r = document.createRange(); r.selectNodeContents(document.getElementById('my-code-v')); var s = getSelection(); s.removeAllRanges(); s.addRange(r); try { document.execCommand('copy'); done(); } catch (x) { } }
  });
})();
