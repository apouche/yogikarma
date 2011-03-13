var Photos = new Hash(
{
	load_preview: function(src)
	{
		$('preview-img').src=src;
	},
	
	thumbnail_clicked: function(event, node)
	{
		src =  event.srcElement.src;
		Photos.load_preview(src.replace(/_\w(\.\w{3})$/, '$1'));
		
	},
	loaded: function()
	{
		//thumbnails = $$('.thumbnail-img');
		//thumbnails.each(function (node) { node.addEventListener('click', Photos.thumbnail_clicked); });
	}
});