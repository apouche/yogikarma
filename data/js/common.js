var Common = new Hash(
{
	'submit': '',
	startRequest : function(form)
	{
		
		var entry = form.id.match(/\d+$/).toString();
		Common.set('submit', $('submit-' + entry).innerHTML);
		$('submit-' + entry).innerHTML = '<img src ="/images/icons/loader.gif" />';
	},
	gotResponse : function(form)
	{
		var entry 		= form.id.match(/\d+$/).toString();
		$('submit-' + entry).innerHTML = Common.get('submit');
		
	},
	updateDOM : function(xml)
	{
		//alert(xml.childNodes.firstChild);
		var tags = xml.childNodes[0];
		for (var i = 0; i < tags.childNodes.length; i++)
		{
			var tag = tags.childNodes[i];
			if (tag.nodeName != '#text')
			{
				$(tag.attributes['id'].nodeValue).innerHTML = Common.xml2Str(tag);
			}
		}
	},
	
	xml2Str: function(node)
 	{
    	try {
	        // Gecko-based browsers, Safari, Opera.
	        return (new XMLSerializer()).serializeToString(node);
	    }
	    catch(e) {
	        try {
	            // Internet Explorer.
	            return node.xml;
	        }
	        catch(e)
	        {
	            //Strange Browser ??
	            alert('Xmlserializer not supported');
	        }
	    }
	    return false;
	},
	
	adjustMainHeight: function()
	{
		var completeHeight = $('complete').offsetHeight - $('top').offsetHeight;
		var mainHeight = $('main-center').offsetHeight;
		mainHeight = completeHeight > mainHeight ? completeHeight: mainHeight;
		var colWidth = $('main-left').offsetWidth;
		$('main').style.height=mainHeight+'px';
		$('top-left').style.width=colWidth+'px';
		$('top-right').style.width=colWidth+'px';
	},
	
	hideTreeLife: function()
	{
		var fx = new Fx.Tween($('tree'), {duration: 1300});
		fx.start('opacity', '0');
	},
	
	loaded: function()
	{
		window.onresize = Common.adjustMainHeight;
		Common.adjustMainHeight();
		//setTimeout("Common.hideTreeLife()", 1500);
	}
});