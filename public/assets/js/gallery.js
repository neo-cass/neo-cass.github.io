/*
  Photo strip lightbox, using PhotoSwipe (vendored in assets/vendor/photoswipe/).

  Progressive enhancement: each thumbnail is a normal link to the full-size image, so
  without JavaScript (or with a modified click such as cmd/ctrl-click) it simply opens
  the file. With JavaScript, a plain click opens the lightbox: previous/next arrows,
  keyboard arrows, swipe, Esc to close, pinch/double-click to zoom, and a caption taken
  from each image's alt text.

  Each link carries data-pswp-width / data-pswp-height (the full-size pixel dimensions),
  which PhotoSwipe needs to lay out the image before it has loaded.
*/
import PhotoSwipeLightbox from '/assets/vendor/photoswipe/photoswipe-lightbox.esm.min.js';

const lightbox = new PhotoSwipeLightbox({
  gallery: '.photo-strip',
  children: 'a',
  pswpModule: () => import('/assets/vendor/photoswipe/photoswipe.esm.min.js'),
  bgOpacity: 1,                    // fully opaque: no page text ghosting through behind the photo
  closeTitle: 'Close',
  zoomTitle: 'Zoom',
  arrowPrevTitle: 'Previous photo',
  arrowNextTitle: 'Next photo',
  errorMsg: 'This photo could not be loaded.'
});

// Caption = the thumbnail's alt text (textContent, never HTML).
lightbox.on('uiRegister', () => {
  lightbox.pswp.ui.registerElement({
    name: 'caption',
    order: 9,
    isButton: false,
    appendTo: 'root',
    onInit: (element, pswp) => {
      pswp.on('change', () => {
        const link = pswp.currSlide.data.element;
        const image = link && link.querySelector('img');
        element.textContent = image ? image.alt : '';
      });
    }
  });
});

lightbox.init();
