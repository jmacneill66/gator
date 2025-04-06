package auth

import (
	"errors"
	"net/http"
	"testing"
)

func TestGetAPIKey(t *testing.T) {
	tests := map[string]struct {
		headers http.Header
		wantKey string
		wantErr error
	}{
		"valid ApiKey header": {
			headers: func() http.Header {
				h := http.Header{}
				h.Set("Authorization", "ApiKey my-secret-key")
				return h
			}(),
			wantKey: "my-secret-key",
			wantErr: nil,
		},
		"no Authorization header": {
			headers: http.Header{},
			wantKey: "",
			wantErr: ErrNoAuthHeaderIncluded,
		},
		"malformed header with wrong prefix": {
			headers: func() http.Header {
				h := http.Header{}
				h.Set("Authorization", "Bearer some-token")
				return h
			}(),
			wantKey: "",
			wantErr: errors.New("malformed authorization header"),
		},
		"malformed header with missing key": {
			headers: func() http.Header {
				h := http.Header{}
				h.Set("Authorization", "ApiKey")
				return h
			}(),
			wantKey: "",
			wantErr: errors.New("malformed authorization header"),
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			gotKey, gotErr := GetAPIKey(tc.headers)

			if gotKey != tc.wantKey {
				t.Fatalf("expected API key %q, got %q", tc.wantKey, gotKey)
			}

			if (gotErr == nil) != (tc.wantErr == nil) || (gotErr != nil && gotErr.Error() != tc.wantErr.Error()) {
				t.Fatalf("expected error %v, got %v", tc.wantErr, gotErr)
			}
		})
	}
}
