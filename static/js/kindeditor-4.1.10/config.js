/**
 * Created by liushuihe@live.com on 2017/3/20.
 */
KindEditor.ready(function(K) {
                K.create('textarea[name=content]',{
                    width:'800px',
                    height:'200px',
                    uploadJson: '/admin/upload/kindeditor',
                });
        });
