<?php
class _0x8b1a99_ {
    private $_0xb06893_;
    public function __construct($_0xb06893_) {
        $this->_0xb06893_ = $_0xb06893_;
    }
    public function __call($method, $args) {
        if ($method === 'say') {
            if (count($args) === 1) {
                echo $args[0];
            }
        }
    }
    public function __destruct() {
        echo $this->_0xb06893_;
    }
}

$data = "TzoxMDoiXzB4OGIxYTk5XyI6MTp7czoyMjoiAF8weDhiMWE5OV8AXzB4YjA2ODkzXyI7czozNDoiZmxhZ3swS195MHVfYzRuX1J1bl83aDFzX3BIcF9mMWwzfSI7fQ==";
unserialize(base64_decode($data));
//$a = new _0x8b1a99_("flag{0K_y0u_c4n_Run_7h1s_pHp_f1l3}");
//echo base64_encode(serialize($a));