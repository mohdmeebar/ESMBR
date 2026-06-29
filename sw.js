// Service Worker — استراتيجية "الشبكة أولاً" لضمان ظهور آخر تحديث دائماً
// غيّر رقم الإصدار عند كل تحديث مهم لإجبار المتصفح على تجديد الكاش
const CACHE = 'esmbr-v3';

// تفعيل فوري للنسخة الجديدة
self.addEventListener('message', function (e) {
  if (e.data === 'skipWaiting') self.skipWaiting();
});

self.addEventListener('install', function (e) {
  // فعّل النسخة الجديدة فوراً بدون انتظار
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    (async function () {
      // احذف كل الكاشات القديمة
      const keys = await caches.keys();
      await Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k);
      }));
      // تحكّم بكل الصفحات المفتوحة فوراً
      await self.clients.claim();
    })()
  );
});

self.addEventListener('fetch', function (e) {
  const req = e.request;

  // لا تتدخل في طلبات Firebase أو الطلبات غير GET
  if (req.method !== 'GET' || req.url.indexOf('firestore') !== -1 ||
      req.url.indexOf('googleapis') !== -1 || req.url.indexOf('gstatic') !== -1) {
    return;
  }

  // الشبكة أولاً: جرّب جلب أحدث نسخة، وإن فشلت الشبكة استخدم الكاش
  e.respondWith(
    fetch(req).then(function (res) {
      // خزّن نسخة محدّثة في الكاش للاستخدام دون إنترنت
      const copy = res.clone();
      caches.open(CACHE).then(function (c) { c.put(req, copy); });
      return res;
    }).catch(function () {
      return caches.match(req);
    })
  );
});
