// Service Worker - إدارة ضيوف الحفل PWA
const CACHE_NAME = 'esmbr-v1';
const ASSETS = [
  './',
  './index-29.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

// التثبيت: تخزين الملفات الأساسية
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS).catch(function(err) {
        // تجاهل الأخطاء لو ملف مو موجود
        console.warn('SW cache partial:', err);
      });
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

// التفعيل: حذف الكاش القديم
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; })
            .map(function(k) { return caches.delete(k); })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

// الجلب: الشبكة أولاً ثم الكاش (Network-first)
// مهم: عشان بيانات Firebase والمكتبات الخارجية تجي محدّثة دائماً
self.addEventListener('fetch', function(e) {
  var req = e.request;

  // تجاهل الطلبات غير GET وطلبات Firebase/الخارجية (نخليها تمر مباشرة للشبكة)
  if (req.method !== 'GET') return;

  var url = new URL(req.url);
  var sameOrigin = url.origin === self.location.origin;

  // ملفات من نفس الموقع: network-first مع fallback للكاش (يشتغل أوفلاين)
  if (sameOrigin) {
    e.respondWith(
      fetch(req).then(function(res) {
        var copy = res.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(req, copy);
        });
        return res;
      }).catch(function() {
        return caches.match(req).then(function(cached) {
          return cached || caches.match('./index-29.html');
        });
      })
    );
  }
  // الملفات الخارجية (CDN، Firebase، الخطوط): الشبكة مباشرة، كاش كاحتياط
  else {
    e.respondWith(
      fetch(req).catch(function() {
        return caches.match(req);
      })
    );
  }
});
